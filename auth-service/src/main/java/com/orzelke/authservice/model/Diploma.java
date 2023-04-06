package com.orzelke.authservice.model;


import com.orzelke.authservice.enums.DiplomaType;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Data
public class Diploma {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    private String title;
    private LocalDate dateOfDefence;
    @Enumerated(EnumType.STRING)
    private DiplomaType diplomaType;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "APPLICATION_USER_ID")
    private ApplicationUser owner;


}
