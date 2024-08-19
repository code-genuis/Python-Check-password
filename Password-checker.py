import subprocess


def get_saved_wifi_passwords():
    # Get the list of WiFi profiles saved on the PC
    profiles_data = (
        subprocess.check_output(["netsh", "wlan", "show", "profiles"])
        .decode("utf-8", errors="backslashreplace")
        .split("\n")
    )

    # Extract profile names
    profiles = [i.split(":")[1][1:-1] for i in profiles_data if "All User Profile" in i]

    wifi_list = []

    # Check if profiles are found
    if len(profiles) != 0:
        for profile in profiles:
            wifi_profile = {}
            # Get the details of the profile
            profile_info = (
                subprocess.check_output(
                    ["netsh", "wlan", "show", "profile", profile, "key=clear"]
                )
                .decode("utf-8", errors="backslashreplace")
                .split("\n")
            )
            wifi_profile["SSID"] = profile

            # Look for the password in the profile details
            for line in profile_info:
                if "Key Content" in line:
                    wifi_profile["Password"] = line.split(":")[1][1:-1]
                    break
            else:
                wifi_profile["Password"] = None

            wifi_list.append(wifi_profile)

    return wifi_list


if __name__ == "__main__":
    wifi_passwords = get_saved_wifi_passwords()

    if wifi_passwords:
        for wifi in wifi_passwords:
            print(f"SSID: {wifi['SSID']}, Password: {wifi['Password']}")
    else:
        print("No WiFi profiles found.")
