package com.orzelke.authservice.repository;
import com.orzelke.authservice.model.AuthenticationProfile;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AuthenticationProfileRepository extends JpaRepository<AuthenticationProfile, Long> {
}
