package com.orzelke.authservice.dto;

import com.orzelke.authservice.enums.DiplomaType;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class DiplomaDTO {
    private String title;
    private LocalDate dateOfDefence;
    private DiplomaType diplomaType;
}

