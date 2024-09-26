<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "tour";

// Create a connection
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check if the connection is successful
if ($conn) {
    echo "Connected successfully";
} else {
    echo "Connection failed: " . mysqli_connect_error();
}

// Initialize an array for storing errors
$errors = [];

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST['username']);
    $email = trim($_POST['email']);
    $password = trim($_POST['password']);
    $confirm_password = trim($_POST['confirm_password']);

    // Basic validation
    if (empty($username) || empty($email) || empty($password) || empty($confirm_password)) {
        $errors[] = "All fields are required.";
    } elseif ($password !== $confirm_password) {
        $errors[] = "Passwords do not match.";
    }

    // If no errors, proceed with registration
    if (empty($errors)) {
        // Hash the password for security
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);

        // Prepare and execute MySQL query to insert data
        $sql = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)";
        $stmt = $conn->prepare($sql);

        if ($stmt) {
            $stmt->bind_param("sss", $username, $email, $hashed_password);

            if ($stmt->execute()) {
                // Registration successful, redirect to login page or success message
                header("Location: login.php");
                exit();
            } else {
                $errors[] = "Error: " . $stmt->error;
            }

            $stmt->close();
        } else {
            $errors[] = "Failed to prepare SQL statement: " . $conn->error;
        }

        // Close the connection
        $conn->close();
    }
}
?>
