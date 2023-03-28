package com.orzelke.authservice.controller;

import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/diploma")
public class DiplomaController {

    @GetMapping
    @SecurityRequirement(name = "Bearer Authentication")
    public ResponseEntity<String> getDiplomaInfo() {
        return ResponseEntity.ok("Good job!");
    }
}
