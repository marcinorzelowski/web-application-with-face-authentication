package com.orzelke.authservice.dto;

import com.orzelke.authservice.enums.FeatureType;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@ToString
@AllArgsConstructor
@NoArgsConstructor
public class FeatureDTO {
    private float value;
    private FeatureType type;
}
