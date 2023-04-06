package com.orzelke.authservice.service;

import com.orzelke.authservice.client.FaceRecognitionClient;
import com.orzelke.authservice.dto.FeatureDTO;
import com.orzelke.authservice.model.ApplicationUser;
import com.orzelke.authservice.model.Feature;
import com.orzelke.authservice.repository.ApplicationUserRepository;
import lombok.RequiredArgsConstructor;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class FaceRecognitionService {
    private static final Logger logger = LoggerFactory.getLogger(FaceRecognitionService.class);
    private final FaceRecognitionClient faceRecognitionClient;
    private final ApplicationUserRepository applicationUserRepository;

    public boolean validateFace(MultipartFile file) {
        List<FeatureDTO> features = faceRecognitionClient.processImage(file).getBody();
        logger.info("Loaded features: {}", features);
        return true;
    }

    public List<Feature> getFaceFeatures(MultipartFile[] images, ApplicationUser savedUser) {
        List<FeatureDTO> features = faceRecognitionClient.processImages(images).getBody();

        return features.stream().map(featureDTO -> Feature.builder()
                .value(featureDTO.getValue())
                .type(featureDTO.getType())
                .user(savedUser)
                .build()).collect(Collectors.toList());
    }
}
