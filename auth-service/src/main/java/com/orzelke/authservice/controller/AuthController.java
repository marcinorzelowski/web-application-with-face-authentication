package com.orzelke.authservice.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.orzelke.authservice.dto.AuthenticationRequest;
import com.orzelke.authservice.dto.AuthenticationResponse;
import com.orzelke.authservice.dto.RegisterRequest;
import com.orzelke.authservice.service.AuthenticationService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@CrossOrigin(origins = "http://localhost:4200")
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthenticationService authenticationService;
    private final ObjectMapper objectMapper;

    @PostMapping(value = "/register", consumes = "multipart/form-data")
    public ResponseEntity<AuthenticationResponse> registerUser(
            @RequestParam("register_data") String registerData,
            @RequestPart("images") MultipartFile[] images) throws JsonProcessingException {
        RegisterRequest request = objectMapper.readValue(registerData, RegisterRequest.class);
        return ResponseEntity.ok(authenticationService.register(request, images));
    }

    @PostMapping(value = "/login", consumes="multipart/form-data")
    public ResponseEntity<AuthenticationResponse> login(
            @RequestParam("user") String user,
            @RequestPart("image") MultipartFile image
    ) throws JsonProcessingException {
        AuthenticationRequest request = objectMapper.readValue(user, AuthenticationRequest.class);
        return ResponseEntity.ok(authenticationService.login(request, image));
    }


}
