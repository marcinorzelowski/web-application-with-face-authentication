package com.orzelke.authservice.controller;

import com.orzelke.authservice.dto.AuthenticationRequest;
import com.orzelke.authservice.dto.AuthenticationResponse;
import com.orzelke.authservice.dto.LoginRequest;
import com.orzelke.authservice.dto.RegisterRequest;
import com.orzelke.authservice.service.AuthenticationService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthenticationService authenticationService;

    @PostMapping("/register")
    public ResponseEntity<AuthenticationResponse> registerUser(@RequestBody RegisterRequest request) {
        return ResponseEntity.ok(authenticationService.register(request));
    }

    @PostMapping("/login")
    public ResponseEntity<AuthenticationResponse> login(@RequestBody AuthenticationRequest request) {
        return ResponseEntity.ok(authenticationService.login(request));
    }


}
