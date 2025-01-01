<?php
// Check if the request is a POST request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the user's reCAPTCHA response from the request
    $recaptchaResponse = $_POST['recaptchaResponse'] ?? '';

    if (empty($recaptchaResponse)) {
        echo json_encode(['success' => false, 'message' => 'reCAPTCHA response is missing.']);
        exit;
    }

    // Your secret key (store it securely using environment variables in production)
    $secretKey = getenv('RECAPTCHA_SECRET');
    if (!$secretKey) {
        echo json_encode(['success' => false, 'message' => 'Secret key not configured.']);
        exit;
    }

    // Google reCAPTCHA verification API URL
    $googleVerifyUrl = 'https://www.google.com/recaptcha/api/siteverify';

    // Send a POST request to Google's reCAPTCHA server
    $response = file_get_contents(
        $googleVerifyUrl . '?secret=' . urlencode($secretKey) . '&response=' . urlencode($recaptchaResponse)
    );

    // Parse the JSON response from Google
    $verification = json_decode($response, true);

    if ($verification['success']) {
        echo json_encode(['success' => true, 'message' => 'Verification successful.']);
    } else {
        echo json_encode(['success' => false, 'message' => 'Verification failed.', 'error_codes' => $verification['error-codes'] ?? []]);
    }
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid request method.']);
}
?>
