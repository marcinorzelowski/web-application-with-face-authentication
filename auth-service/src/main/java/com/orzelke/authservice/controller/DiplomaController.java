package com.orzelke.authservice.controller;

import com.orzelke.authservice.dto.DiplomaDTO;
import com.orzelke.authservice.enums.DiplomaType;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;

@RestController
@CrossOrigin(origins = "http://localhost:4200")
@RequestMapping("/api/diploma")
@RequiredArgsConstructor
public class DiplomaController {

    @GetMapping
    public DiplomaDTO getExampleDiploma() {
        return DiplomaDTO.builder()
                .diplomaType(DiplomaType.MASTER)
                .dateOfDefence(LocalDate.now())
                .title("System uwierzytelniania wieloczynnikowego z wykorzystaniem technik rozpoznawania twarzy")
                .build();
    }
}
