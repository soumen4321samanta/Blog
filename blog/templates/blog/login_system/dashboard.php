<?php
session_start();

// Check if the user is logged in by verifying if session variables are set
if (!isset($_SESSION['username']) || !isset($_SESSION['email'])) {
    // If the user is not logged in, redirect to the login page
    header("Location: login.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Dashboard</title>
    <link rel="stylesheet" href="styles1.css">
</head>
<body>
    <div class="dashboard-container">
        <h1>Welcome, <?php echo htmlspecialchars($_SESSION['username']); ?>!</h1>
        <p>Your email: <?php echo htmlspecialchars($_SESSION['email']); ?></p>

        <div class="dashboard-menu">
            <a href="edit_profile.php" class="dashboard-btn">Edit Profile</a>
            <a href="change_password.php" class="dashboard-btn">Change Password</a>
            <form action="logout.php" method="POST" class="logout-form">
                <button type="submit" name="logout" class="dashboard-btn logout-btn">Logout</button>
            </form>
        </div>
    </div>
</body>
</html>
