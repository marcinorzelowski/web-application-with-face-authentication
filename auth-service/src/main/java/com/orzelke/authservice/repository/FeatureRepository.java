package com.orzelke.authservice.repository;

import com.orzelke.authservice.model.Feature;
import org.springframework.data.jpa.repository.JpaRepository;

public interface FeatureRepository extends JpaRepository<Feature, Long> {
}
