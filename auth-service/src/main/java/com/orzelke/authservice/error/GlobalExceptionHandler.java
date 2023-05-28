package com.orzelke.authservice.error;

import com.orzelke.authservice.dto.ExceptionResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(IncorrectNumberOfFacesException.class)
    public ResponseEntity<ExceptionResponse> handleIncorrectNumberOfFacesException(IncorrectNumberOfFacesException e) {
        return new ResponseEntity<>(new ExceptionResponse(e.getMessage()), HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(FaceNotDetectedException.class)
    public ResponseEntity<ExceptionResponse> handleFaceNotDetectedException(FaceNotDetectedException e) {
        return new ResponseEntity<>(new ExceptionResponse(e.getMessage()), HttpStatus.BAD_REQUEST);
    }
    @ExceptionHandler(AuthException.class)
    public ResponseEntity<ExceptionResponse> handleAuthException(AuthException e) {
        return new ResponseEntity<>(new ExceptionResponse(e.getMessage()), HttpStatus.BAD_REQUEST);
    }
    @ExceptionHandler(RegistrationException.class)
    public ResponseEntity<ExceptionResponse> handleRegistrationException(RegistrationException e) {
        return new ResponseEntity<>(new ExceptionResponse(e.getMessage()), HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(UnknownException.class)
    public ResponseEntity<ExceptionResponse> handleUnknownException(UnknownException e) {
        return new ResponseEntity<>(new ExceptionResponse(e.getMessage()), HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
