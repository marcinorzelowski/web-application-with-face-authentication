
package com.orzelke.authservice.utils;

import org.apache.commons.math3.distribution.MultivariateNormalDistribution;
import org.apache.commons.math3.linear.*;
import org.apache.commons.math3.stat.correlation.Covariance;

public class MathUtils {

    public static double computeGmd(double[] f1, double[] f2) {
        // Create the mixture model for the first feature vector
        MultivariateNormalDistribution[] mixture1 = createMixtureModel(f1);

        // Create the mixture model for the second feature vector
        MultivariateNormalDistribution[] mixture2 = createMixtureModel(f2);

        // Compute the Bhattacharyya coefficient between the two mixture models
        double bc = computeBhattacharyyaCoeff(mixture1, mixture2);

        // Compute the Gaussian mixture distance
        double gmd = -Math.log(bc);

        return gmd;
    }

    public static MultivariateNormalDistribution[] createMixtureModel(double[] features) {
        int k = 2; // number of Gaussian components
        int d = features.length; // dimensionality of feature space

        // Initialize the mixture model parameters
        double[] weights = {0.5, 0.5}; // equal weights for both components
        double[][] means = {features, features}; // both components have the same mean
        double[][][] covariances = new double[k][d][d]; // the covariance matrices will be diagonal

        // Compute the diagonal covariance matrix for each component
        for (int j = 0; j < k; j++) {
            for (int l = 0; l < d; l++) {
                covariances[j][l][l] = 1.0; // set the diagonal entries to 1.0
            }
        }

        // Create the Gaussian components of the mixture model
        MultivariateNormalDistribution[] gaussians = new MultivariateNormalDistribution[k];
        for (int j = 0; j < k; j++) {
            gaussians[j] = new MultivariateNormalDistribution(means[j], MatrixUtils.createRealMatrix(covariances[j]).getData());
        }

        return gaussians;
    }

    public static double computeBhattacharyyaCoeff(MultivariateNormalDistribution[] mixture1, MultivariateNormalDistribution[] mixture2) {
        int k = mixture1.length;

        // Compute the Bhattacharyya coefficient
        double sum = 0.0;
        for (int j = 0; j < k; j++) {
            sum += Math.sqrt(mixture1[j].density(mixture1[j].getMeans()) * mixture2[j].density(mixture2[j].getMeans()));
        }
        double bc = sum / Math.sqrt(2.0);

        return bc;
    }

    public double manhattanDistance(double[] vectorA, double[] vectorB) {
        double distance = 0;

        for (int i = 0; i < vectorA.length; i++) {
            distance += Math.abs(vectorA[i] - vectorB[i]);
        }

        return distance;
    }

    public static double cosineDistance(double[] vectorA, double[] vectorB) {
        double dotProduct = 0;
        double magnitudeA = 0;
        double magnitudeB = 0;

        for (int i = 0; i < vectorA.length; i++) {
            dotProduct += vectorA[i] * vectorB[i];
            magnitudeA += Math.pow(vectorA[i], 2);
            magnitudeB += Math.pow(vectorB[i], 2);
        }

        double cosineSimilarity = dotProduct / (Math.sqrt(magnitudeA) * Math.sqrt(magnitudeB));
        double cosineDistance = 1 - cosineSimilarity;

        return cosineDistance;
    }

    public static double mahalanobisDistance(double[] vectorA, double[] vectorB, double[][] dataset) {
        RealMatrix matrix = MatrixUtils.createRealMatrix(dataset);
        RealMatrix covarianceMatrix = new Covariance(matrix).getCovarianceMatrix();

        // Compute the inverse covariance matrix
        RealMatrix inverseCovarianceMatrix;
        try {
            inverseCovarianceMatrix = new LUDecomposition(covarianceMatrix).getSolver().getInverse();
        } catch (SingularMatrixException e) {
            // In case the matrix is singular, use SVD to compute the pseudo-inverse
            SingularValueDecomposition svd = new SingularValueDecomposition(covarianceMatrix);
            inverseCovarianceMatrix = svd.getSolver().getInverse();
        }

        // Calculate the difference between the two vectors
        double[] diff = new double[vectorA.length];
        for (int i = 0; i < vectorA.length; i++) {
            diff[i] = vectorA[i] - vectorB[i];
        }

        // Calculate the Mahalanobis distance
        RealMatrix diffMatrix = MatrixUtils.createRowRealMatrix(diff);
        RealMatrix resultMatrix = diffMatrix.multiply(inverseCovarianceMatrix).multiply(diffMatrix.transpose());

        return Math.sqrt(resultMatrix.getEntry(0, 0));
    }
}
