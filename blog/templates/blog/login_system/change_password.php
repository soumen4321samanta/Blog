<?php
session_start();

// Ensure the user is logged in
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "tour";

// Connect to the database
$conn = mysqli_connect($servername, $username, $password, $dbname);
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Fetch the current user's data (assuming 'username' is in the session)
$current_username = $_SESSION['username'];
$errors = [];

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $current_password = trim($_POST['current_password']);
    $new_password = trim($_POST['new_password']);
    $confirm_password = trim($_POST['confirm_password']);

    // Validate the form
    if (empty($current_password) || empty($new_password) || empty($confirm_password)) {
        $errors[] = "All fields are required.";
    } elseif ($new_password !== $confirm_password) {
        $errors[] = "New passwords do not match.";
    }

    // If no errors, proceed
    if (empty($errors)) {
        // Get the current password from the database
        $sql = "SELECT password FROM users WHERE username = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("s", $current_username);
        $stmt->execute();
        $stmt->store_result();

        if ($stmt->num_rows > 0) {
            $stmt->bind_result($stored_password_hash);
            $stmt->fetch();

            // Verify if the current password is correct
            if (password_verify($current_password, $stored_password_hash)) {
                // Hash the new password
                $hashed_new_password = password_hash($new_password, PASSWORD_DEFAULT);

                // Update the password in the database
                $update_sql = "UPDATE users SET password = ? WHERE username = ?";
                $update_stmt = $conn->prepare($update_sql);
                $update_stmt->bind_param("ss", $hashed_new_password, $current_username);

                if ($update_stmt->execute()) {
                    echo "Password successfully updated!";
                    // Optionally, redirect to dashboard or logout after password change
                    // header("Location: dashboard.php");
                    // exit();
                } else {
                    $errors[] = "Error updating password: " . $update_stmt->error;
                }

                $update_stmt->close();
            } else {
                $errors[] = "Current password is incorrect.";
            }
        } else {
            $errors[] = "User not found.";
        }

        $stmt->close();
    }
}

$conn->close();
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Change Password</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="change-password-container">
        <h2>Change Password</h2>
        <form action="change_password.php" method="POST">
            <div class="form-group">
                <label for="current_password">Current Password</label>
                <input type="password" id="current_password" name="current_password" required>
            </div>

            <div class="form-group">
                <label for="new_password">New Password</label>
                <input type="password" id="new_password" name="new_password" required>
            </div>

            <div class="form-group">
                <label for="confirm_password">Confirm New Password</label>
                <input type="password" id="confirm_password" name="confirm_password" required>
            </div>

            <button type="submit" class="change-password-btn">Update Password</button>
        </form>
    </div>
</body>
</html>
