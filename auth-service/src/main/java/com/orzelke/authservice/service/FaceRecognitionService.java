package com.orzelke.authservice.service;

import com.orzelke.authservice.client.FaceRecognitionClient;
import com.orzelke.authservice.dto.FeatureDTO;
import com.orzelke.authservice.enums.FeatureType;
import com.orzelke.authservice.mapper.FeatureMapper;
import com.orzelke.authservice.model.ApplicationUser;
import com.orzelke.authservice.model.Feature;
import com.orzelke.authservice.repository.ApplicationUserRepository;
import com.orzelke.authservice.repository.FeatureRepository;
import com.orzelke.authservice.utils.MathUtils;
import lombok.RequiredArgsConstructor;

import org.apache.commons.math3.ml.distance.EuclideanDistance;
import org.apache.commons.math3.ml.distance.ManhattanDistance;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class FaceRecognitionService {
    private static final Logger logger = LoggerFactory.getLogger(FaceRecognitionService.class);
    private final FaceRecognitionClient faceRecognitionClient;
    private final FeatureMapper featureMapper;
    private final ApplicationUserRepository applicationUserRepository;

    private static final float THRESHOLD = 96.00F;

    public boolean isFaceRecognized(MultipartFile file, ApplicationUser user) {
        List<FeatureDTO> calculatedFeatures = faceRecognitionClient.processImage(file).getBody();
        List<FeatureDTO> featuresFromDatabase = user.getFeatures().stream().map(featureMapper::toDTO).toList();

        logger.info("Loaded features: {}", calculatedFeatures);
        logger.info("User features: {}", featuresFromDatabase);

        double finalMatching = 100 - calculateMatchingScore(featuresFromDatabase, calculatedFeatures);
        logger.info("Final Matching is equal: {} %", finalMatching);
        return finalMatching > THRESHOLD;
    }

    public List<Feature> getFaceFeatures(MultipartFile[] images, ApplicationUser savedUser) {
        List<FeatureDTO> features = faceRecognitionClient.processImages(images).getBody();

        return features.stream().map(featureDTO -> Feature.builder()
                .value(featureDTO.getValue())
                .type(featureDTO.getType())
                .user(savedUser)
                .build()).collect(Collectors.toList());
    }

    private double calculateMatchingScore(List<FeatureDTO> dbFeatures, List<FeatureDTO> imgFeatures) {
        validateFeatures(dbFeatures, imgFeatures);

        //sort
        double[] dbFeaturesValues = dbFeatures.stream()
                .sorted(Comparator.comparing(FeatureDTO::getType))
                .mapToDouble(FeatureDTO::getValue)
                .toArray();
        double[] imgFeaturesValues = imgFeatures.stream()
                .sorted(Comparator.comparing(FeatureDTO::getType))
                .mapToDouble(FeatureDTO::getValue)
                .toArray();

        getClosestEuclidean(imgFeaturesValues);
        getClosestManhattan(imgFeaturesValues);
        getClosestMahalanobis(imgFeaturesValues);

        logger.info("Manhattan distance: {}, EuclideanDistance: {}, Cosine distance: {}, Mahalanobis Distance: {}", new ManhattanDistance().compute(dbFeaturesValues, imgFeaturesValues),
                new EuclideanDistance().compute(dbFeaturesValues, imgFeaturesValues), MathUtils.cosineDistance(imgFeaturesValues, dbFeaturesValues), MathUtils.mahalanobisDistance(imgFeaturesValues, dbFeaturesValues, getDatabase()));

        return MathUtils.computeGmd(dbFeaturesValues, imgFeaturesValues);
    }

    private void getClosestEuclidean(double[] imgFeaturesValues) {
        double minVal = 3000;
        String minName = "NONE";
        List<ApplicationUser> allUsers = applicationUserRepository.findAll();
        for (ApplicationUser applicationUser : allUsers) {
            double[] vector = applicationUser.getFeatures().stream()
                    .map(featureMapper::toDTO)
                    .sorted(Comparator.comparing(FeatureDTO::getType))
                    .mapToDouble(FeatureDTO::getValue)
                    .toArray();

            double distance = new EuclideanDistance().compute(vector, imgFeaturesValues);
            if (distance < minVal) {
                minVal = distance;
                minName = applicationUser.getFirstName();
            }
        }
        logger.info("Euclidean distance closest to {} with distance {}", minName, minVal);
    }

    private void getClosestManhattan(double[] imgFeaturesValues) {
        double minVal = 3000;
        String minName = "NONE";
        List<ApplicationUser> allUsers = applicationUserRepository.findAll();
        for (ApplicationUser applicationUser : allUsers) {
            double[] vector = applicationUser.getFeatures().stream()
                    .map(featureMapper::toDTO)
                    .sorted(Comparator.comparing(FeatureDTO::getType))
                    .mapToDouble(FeatureDTO::getValue)
                    .toArray();

            double distance = new ManhattanDistance().compute(vector, imgFeaturesValues);
            if (distance < minVal) {
                minVal = distance;
                minName = applicationUser.getFirstName();
            }
        }
        logger.info("Manhattan distance closest to {} with distance {}", minName, minVal);
    }

    private void getClosestMahalanobis(double[] imgFeaturesValues) {
        double minVal = 3000;
        String minName = "NONE";
        List<ApplicationUser> allUsers = applicationUserRepository.findAll();
        for (ApplicationUser applicationUser : allUsers) {
            double[] vector = applicationUser.getFeatures().stream()
                    .map(featureMapper::toDTO)
                    .sorted(Comparator.comparing(FeatureDTO::getType))
                    .mapToDouble(FeatureDTO::getValue)
                    .toArray();

            double distance = MathUtils.mahalanobisDistance(vector, imgFeaturesValues, getDatabase());
            if (distance < minVal) {
                minVal = distance;
                minName = applicationUser.getFirstName();
            }
        }
        logger.info("Mahalanobis distance closest to {} with distance {}", minName, minVal);
    }

    private double[][] getDatabase() {
        List<ApplicationUser> allUsers = applicationUserRepository.findAll();
        double[][] database = new double[allUsers.size()][];

        for (int i = 0; i < allUsers.size(); i++) {
            ApplicationUser applicationUser = allUsers.get(i);

            double[] vector = applicationUser.getFeatures().stream()
                    .map(featureMapper::toDTO)
                    .sorted(Comparator.comparing(FeatureDTO::getType))
                    .mapToDouble(FeatureDTO::getValue)
                    .toArray();
            database[i] = vector;
        }

        return database;
    }



    private void validateFeatures(List<FeatureDTO> dbFeatures, List<FeatureDTO> imgFeatures) {
        if (dbFeatures.size() != imgFeatures.size()) {
            logger.error("Wrong features");
        }
        HashSet<FeatureType> dbFeaturesTypes = dbFeatures.stream().map(FeatureDTO::getType).collect(Collectors.toCollection(HashSet::new));
        HashSet<FeatureType> imgFeatureTypes = imgFeatures.stream().map(FeatureDTO::getType).collect(Collectors.toCollection(HashSet::new));

        if (!dbFeaturesTypes.equals(imgFeatureTypes)) {
            logger.error("Wrong");
        }
    }
}
