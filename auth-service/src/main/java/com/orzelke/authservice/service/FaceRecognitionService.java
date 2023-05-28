package com.orzelke.authservice.service;

import com.orzelke.authservice.client.FaceRecognitionClient;
import com.orzelke.authservice.error.FaceNotDetectedException;
import com.orzelke.authservice.model.ApplicationUser;
import com.orzelke.authservice.model.AuthenticationProfile;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.apache.commons.math3.ml.distance.EuclideanDistance;
import org.apache.commons.math3.ml.distance.ManhattanDistance;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.stream.IntStream;

@Service
@RequiredArgsConstructor
@Transactional
public class FaceRecognitionService {
    private final FaceRecognitionClient faceRecognitionClient;
    public AuthenticationProfile createProfile(
            MultipartFile[] images,
            ApplicationUser user) {
        try {
            List<List<Double>> featuresVectors = faceRecognitionClient
                    .processImages(images)
                    .getBody();
            double[] meanVector = calculateMeanVector(featuresVectors);

            return AuthenticationProfile.builder()
                    .user(user)
                    .vector(Arrays.toString(meanVector))
                    .threshold(calculateThreshold(meanVector, featuresVectors))
                    .build();
        } catch (Exception e) {
            throw new FaceNotDetectedException("Could not detect faces on images.");
        }

    }

    private double calculateThreshold(
            double[] meanVector,
            List<List<Double>> featuresVectors) {
        ManhattanDistance manhattanDistance = new ManhattanDistance();
        List<Double> distances = new ArrayList<>();
        for (List<Double> vector : featuresVectors) {
            double[] vectorDouble = vector
                    .stream()
                    .mapToDouble(Double::doubleValue)
                    .toArray();
            distances.add(manhattanDistance.compute(meanVector, vectorDouble));
        }
        return distances.stream().max(Double::compareTo)
                .orElse(distances.get(0));
    }

    private double[] calculateMeanVector(List<List<Double>> featuresVectors) {
        int vectorSize = featuresVectors.get(0).size();
        return IntStream.range(0, vectorSize)
                .mapToDouble(i -> featuresVectors.stream()
                        .mapToDouble(value -> value.get(i))
                        .average().getAsDouble())
                .toArray();
    }


    public boolean isFaceRecognized(MultipartFile image, ApplicationUser user) {
        try {
            List<Double> faceFeatures = faceRecognitionClient
                    .processImage(image)
                    .getBody();
            double[] faceVector = faceFeatures.stream()
                    .mapToDouble(Double::doubleValue)
                    .toArray();

            ManhattanDistance manhattanDistance = new ManhattanDistance();

            AuthenticationProfile profile = user.getAuthenticationProfile();
            String vectorString = profile.getVector()
                    .replace("[", "")
                    .replace("]", "")
                    .replace(" ", "");
            double[] meanVector = Arrays.stream(vectorString.split(","))
                    .mapToDouble(Double::parseDouble)
                    .toArray();
            double distance = manhattanDistance.compute(meanVector, faceVector);
            return manhattanDistance
                    .compute(meanVector, faceVector) < profile.getThreshold();
        } catch (Exception e) {
            throw new FaceNotDetectedException("Could not detect faces on image.");
        }

    }
}

