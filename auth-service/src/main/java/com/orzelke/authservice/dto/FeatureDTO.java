package com.orzelke.authservice.dto;

import com.orzelke.authservice.enums.FeatureType;
import lombok.Data;
import lombok.ToString;

@Data
@ToString
public class FeatureDTO {
    private float value;
    private FeatureType type;
}
