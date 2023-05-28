package com.orzelke.authservice.service;

import com.orzelke.authservice.dto.AuthenticationRequest;
import com.orzelke.authservice.dto.AuthenticationResponse;
import com.orzelke.authservice.dto.RegisterRequest;
import com.orzelke.authservice.enums.Role;
import com.orzelke.authservice.error.AuthException;
import com.orzelke.authservice.error.RegistrationException;
import com.orzelke.authservice.model.ApplicationUser;
import com.orzelke.authservice.repository.ApplicationUserRepository;
import com.orzelke.authservice.repository.AuthenticationProfileRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
@RequiredArgsConstructor
@Transactional
public class AuthenticationService {

    private final ApplicationUserRepository repository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;
    private final FaceRecognitionService faceRecognitionService;
    private final AuthenticationProfileRepository authenticationProfileRepository;

    public AuthenticationResponse register(RegisterRequest request, MultipartFile[] images) {
        var exists = repository.findApplicationUserByEmail(request.getEmail()).isPresent();
        if (exists) {
            throw new RegistrationException("User with a given e-mail already exists.");
        }
        var user = ApplicationUser.builder()
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .role(Role.USER)
                .build();

        ApplicationUser savedUser = repository.save(user);
        authenticationProfileRepository.save(faceRecognitionService.createProfile(images, savedUser));


        var jwtToken = jwtService.generateToken(user);
        return AuthenticationResponse.builder()
                .email(user.getEmail())
                .lastName(user.getLastName())
                .firstName(user.getFirstName())
                .token(jwtToken)
                .build();
    }

    public AuthenticationResponse login(AuthenticationRequest request, MultipartFile image) throws Exception {

        var user = repository.findApplicationUserByEmail(request.getEmail())
                .orElseThrow(AuthException::new);
        if (faceRecognitionService.isFaceRecognized(image, user)) {
            authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
            );
            var jwtToken = jwtService.generateToken(user);
            return AuthenticationResponse.builder()
                    .firstName(user.getFirstName())
                    .lastName(user.getLastName())
                    .email(user.getEmail())
                    .token(jwtToken)
                    .build();
        } else {
            throw new AuthException();
        }
    }

}
