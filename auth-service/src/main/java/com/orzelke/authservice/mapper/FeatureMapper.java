package com.orzelke.authservice.mapper;


import com.orzelke.authservice.dto.FeatureDTO;
import com.orzelke.authservice.model.Feature;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper(componentModel = "spring")
public interface FeatureMapper {

    FeatureMapper INSTANCE = Mappers.getMapper(FeatureMapper.class);

    FeatureDTO toDTO(Feature feature);

    Feature toEntity(FeatureDTO dto);
}
