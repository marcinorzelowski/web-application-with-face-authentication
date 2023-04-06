package com.orzelke.authservice.repository;

import com.orzelke.authservice.model.ApplicationUser;
import com.orzelke.authservice.model.Diploma;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface DiplomaRepository extends JpaRepository<Diploma, Long> {
    List<Diploma> getDiplomasByOwner(ApplicationUser owner);
}
