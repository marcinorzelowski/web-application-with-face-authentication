package com.orzelke.authservice.service;

import com.orzelke.authservice.dto.DiplomaDTO;
import com.orzelke.authservice.model.ApplicationUser;
import com.orzelke.authservice.model.Diploma;
import com.orzelke.authservice.repository.DiplomaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class DiplomaService {

    private final DiplomaRepository diplomaRepository;


    public void addDiploma(@RequestBody DiplomaDTO diplomaDTO) {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        ApplicationUser user = (ApplicationUser) authentication.getPrincipal();

        Diploma diploma = Diploma.builder()
                .dateOfDefence(diplomaDTO.getDateOfDefence())
                .diplomaType(diplomaDTO.getDiplomaType())
                .title(diplomaDTO.getTitle())
                .owner(user)
                .build();

        diplomaRepository.save(diploma);
    }

    public List<DiplomaDTO> getDiplomas() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        ApplicationUser user = (ApplicationUser) authentication.getPrincipal();

        return diplomaRepository.getDiplomasByOwner(user).stream().map(
                diploma -> DiplomaDTO.builder()
                        .diplomaType(diploma.getDiplomaType())
                        .dateOfDefence(diploma.getDateOfDefence())
                        .title(diploma.getTitle())
                        .build()
        ).collect(Collectors.toList());
    }
}
