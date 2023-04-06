package com.orzelke.authservice.model;


import com.orzelke.authservice.enums.FeatureType;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Feature {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    private float value;
    @Enumerated(EnumType.STRING)
    private FeatureType type;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "APPLICATION_USER_ID")
    private ApplicationUser user;
}
