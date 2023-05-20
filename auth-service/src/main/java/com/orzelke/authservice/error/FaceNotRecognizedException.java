package com.orzelke.authservice.error;

public class FaceNotRecognizedException extends RuntimeException{
    public FaceNotRecognizedException() {
        super("Face was not recognized");
    }
}
