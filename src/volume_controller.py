"""
Volume controller for Windows using pycaw library.
Provides interface to control system volume.
"""

try:
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False
    print("Warning: pycaw not installed. Volume control will be simulated.")


class VolumeController:
    """Interface for system volume control on Windows."""
    
    def __init__(self):
        """Initialize the volume controller."""
        self.volume_interface = None
        self.simulated_volume = 50  # For simulation mode
        
        if PYCAW_AVAILABLE:
            try:
                # Get the default audio device
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                self.volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
                print("Volume controller initialized successfully")
            except Exception as e:
                print(f"Failed to initialize volume controller: {e}")
                print("Falling back to simulation mode")
                self.volume_interface = None
        else:
            print("Running in simulation mode (install pycaw for real volume control)")
    
    def set_volume(self, level):
        """Set system volume to specified level.
        
        Args:
            level: Volume level (0-100)
        """
        # Clamp to valid range
        level = max(0, min(100, level))
        
        if self.volume_interface:
            try:
                # Convert 0-100 to 0.0-1.0 range
                volume_scalar = level / 100.0
                self.volume_interface.SetMasterVolumeLevelScalar(volume_scalar, None)
            except Exception as e:
                print(f"Error setting volume: {e}")
        else:
            # Simulation mode
            self.simulated_volume = level
            # Uncomment for debugging:
            # print(f"[SIMULATED] Volume set to: {level}%")
    
    def get_volume(self):
        """Get current system volume.
        
        Returns:
            int: Current volume level (0-100)
        """
        if self.volume_interface:
            try:
                current_volume = self.volume_interface.GetMasterVolumeLevelScalar()
                return int(current_volume * 100)
            except Exception as e:
                print(f"Error getting volume: {e}")
                return 50
        else:
            # Simulation mode
            return self.simulated_volume
    
    def mute(self):
        """Mute system audio."""
        if self.volume_interface:
            try:
                self.volume_interface.SetMute(1, None)
            except Exception as e:
                print(f"Error muting: {e}")
        else:
            print("[SIMULATED] Audio muted")
    
    def unmute(self):
        """Unmute system audio."""
        if self.volume_interface:
            try:
                self.volume_interface.SetMute(0, None)
            except Exception as e:
                print(f"Error unmuting: {e}")
        else:
            print("[SIMULATED] Audio unmuted")
    
    def is_muted(self):
        """Check if system audio is muted.
        
        Returns:
            bool: True if muted, False otherwise
        """
        if self.volume_interface:
            try:
                return bool(self.volume_interface.GetMute())
            except Exception as e:
                print(f"Error checking mute status: {e}")
                return False
        else:
            return False
