package com.orzelke.authservice.model;


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
public class AuthenticationProfile {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    @Column(length = 1000)
    private String vector;
    private double threshold;
    @OneToOne
    @JoinColumn(name = "user_id", referencedColumnName = "id")
    private ApplicationUser user;
}
