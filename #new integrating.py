#new integrating 
import example2
import word_library

import threading


# Create threads for each function
eye_tracking_thread = threading.Thread(target=run_example2)
interface_thread = threading.Thread(target=run_word_library)

# Start the threads
eye_tracking_thread.start()
interface_thread.start()

# Wait for both threads to complete
eye_tracking_thread.join()
interface_thread.join()