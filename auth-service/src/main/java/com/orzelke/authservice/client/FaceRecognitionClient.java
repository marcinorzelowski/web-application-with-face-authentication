package com.orzelke.authservice.client;

import com.orzelke.authservice.configuration.FeignClientConfiguration;
import com.orzelke.authservice.dto.FeatureDTO;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.cloud.openfeign.FeignClientProperties;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@FeignClient(configuration = FeignClientConfiguration.class ,name = "faceRecognitionClient", url = "http://localhost:5000/api/face-recognition")
public interface FaceRecognitionClient {

    @PostMapping(value = "/image", consumes = "multipart/form-data")
    ResponseEntity<List<FeatureDTO>> processImage(@RequestPart("image") MultipartFile image);


    @PostMapping(value = "/images", consumes = "multipart/form-data")
    ResponseEntity<List<FeatureDTO>> processImages(@RequestPart("images") MultipartFile[] images);
}
