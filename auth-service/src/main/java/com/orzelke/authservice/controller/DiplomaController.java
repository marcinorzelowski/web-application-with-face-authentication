package com.orzelke.authservice.controller;

import com.orzelke.authservice.dto.DiplomaDTO;
import com.orzelke.authservice.service.DiplomaService;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin(allowedHeaders = "*")
@RequiredArgsConstructor
@RequestMapping("/api/diploma")
public class DiplomaController {


    private final DiplomaService diplomaService;

    @GetMapping
    @SecurityRequirement(name = "Bearer Authentication")
    public ResponseEntity<List<DiplomaDTO>> getDiplomas() {
        return ResponseEntity.ok(diplomaService.getDiplomas());
    }



    @PostMapping
    @SecurityRequirement(name = "Bearer Authentication")
    public ResponseEntity<Void> addDiploma(@RequestBody DiplomaDTO diplomaDTO) {
        diplomaService.addDiploma(diplomaDTO);
        return ResponseEntity.ok().build();
    }
}
