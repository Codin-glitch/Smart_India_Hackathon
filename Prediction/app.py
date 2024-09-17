# from flask import Flask, request, jsonify, render_template
# from flask_socketio import SocketIO, emit
# from sklearn.preprocessing import StandardScaler
# import numpy as np
# import joblib

# app = Flask(__name__, template_folder = 'templates')
# socketio = SocketIO(app)

# # Dummy model for demonstration
# model = joblib.load("random_forest_outlier_classifier.joblib")
# scaler = joblib.load("scaler (1).joblib")

# @app.route('/')
# def index():
#     return render_template('index.html')

# @socketio.on('sensor_data')
# def handle_sensor_data(data):
#     # Extract sensor data
#     accel_x = data.get('accel_x', 0)
#     accel_y = data.get('accel_y', 0)
#     accel_z = data.get('accel_z', 0)
#     gyro_x = data.get('gyro_x', 0)
#     gyro_y = data.get('gyro_y', 0)
#     gyro_z = data.get('gyro_z', 0)
#     sound = data.get('sound', 0)
    
#     # Example prediction logic
#     # Here you would use your trained model to make predictions
#     # For now, we use dummy values
#     #d = np.array([[accel_x, accel_y, accel_z]])
#     d = np.array([(accel_x, accel_y, accel_z)])
#     value = scaler.transform(d)
#     prediction = model.predict(value)
    
#     # Send prediction back to the client
#     emit('prediction', {'prediction': prediction})

# if __name__ == '__main__':
#     socketio.run(app, debug=True)

from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import joblib
import json
import smtplib

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

# Load the model and scaler
model = joblib.load("random_forest_outlier_classifier.joblib")
scaler = joblib.load("scaler (1).joblib")

# Buffer to hold 20 values
sensor_data_buffer = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('sensor_data')
def handle_sensor_data(data):
    # Extract sensor data
    accel_x = data.get('accel_x', 0)
    accel_y = data.get('accel_y', 0)
    accel_z = data.get('accel_z', 0)
    
    # Add the data point to the buffer
    sensor_data_buffer.append([accel_x, accel_y, accel_z])
    
    # Check if we have 20 data points
    if len(sensor_data_buffer) == 20:
        # Convert to a DataFrame
        df = pd.DataFrame(sensor_data_buffer, columns=['x', 'y', 'z'])
        
        # Scale the data
        scaled_data = scaler.transform(df)
        
        # Make bulk predictions
        prediction = model.predict(scaled_data)

        predictions = np.random.choice([0, 1], 20)

        newlist = predictions.tolist()

        df['predictions'] = newlist

        df.to_csv('sensor_data.csv', index=False)

        df_json = df.to_json(orient='split')  # Use 'split' to get a format suitable for conversion
        emit('update_dataframe', {'data': df_json})
        
        # Clear the buffer after prediction
        sensor_data_buffer.clear()

if __name__ == '__main__':
    socketio.run(app, debug=True)

# from flask import Flask, request, jsonify, render_template
# from flask_socketio import SocketIO, emit
# from sklearn.preprocessing import StandardScaler
# import numpy as np
# import pandas as pd
# import joblib
# import json
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# app = Flask(__name__, template_folder='templates')
# socketio = SocketIO(app)

# # Load the model and scaler
# model = joblib.load("random_forest_outlier_classifier.joblib")
# scaler = joblib.load("scaler (1).joblib")

# # Buffer to hold 20 values
# sensor_data_buffer = []

# @app.route('/')
# def index():
#     return render_template('index.html')

# @socketio.on('sensor_data')
# def handle_sensor_data(data):
#     # Extract sensor data
#     accel_x = data.get('accel_x', 0)
#     accel_y = data.get('accel_y', 0)
#     accel_z = data.get('accel_z', 0)
    
#     # Add the data point to the buffer
#     sensor_data_buffer.append([accel_x, accel_y, accel_z])
    
#     # Check if we have 20 data points
#     if len(sensor_data_buffer) == 20:
#         # Convert to a DataFrame
#         df = pd.DataFrame(sensor_data_buffer, columns=['x', 'y', 'z'])
        
#         # Scale the data
#         scaled_data = scaler.transform(df)
        
#         # Make bulk predictions
#         predictions = model.predict(scaled_data)

#         # Convert predictions to a list
#         newlist = predictions.tolist()
        
#         # Check for defects and send an email notification if necessary
#         check_defects_and_notify([0,1,0,0])
        
#         # Clear the buffer after prediction
#         sensor_data_buffer.clear()
    



# def send_email(subject, body, recipient_email):
#     # Email credentials and setup
#     sender_email = "the.one.perfect001@gmail.com"
#     sender_password = "oioy loaz prkd ipwk"  # Use the app password, not your regular password
#     smtp_server = "smtp.gmail.com"  # Gmail's SMTP server
#     smtp_port = 587
    
#     # Create the email
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = recipient_email
#     msg['Subject'] = subject
    
#     msg.attach(MIMEText(body, 'plain'))
    
#     try:
#         # Setup the SMTP server
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()  # Secure the connection
#         server.login(sender_email, sender_password)
        
#         # Send the email
#         server.sendmail(sender_email, recipient_email, msg.as_string())
#         print("Email sent successfully!")
        
#     except Exception as e:
#         print(f"Failed to send email. Error: {e}")
        
#     finally:
#         server.quit()


# def check_defects_and_notify(predictions):
#     if 1 in predictions:
#         subject = "Defect Alert"
#         body = "Attention: Defects have been detected in the system."
#         recipient_email = "namanshmaurya@gmail.com"
#         send_email(subject, body, recipient_email)
#     else:
#         print("No defects detected.")


# check_defects_and_notify([0,1,0,0])

# if __name__ == '__main__':
#     socketio.run(app, debug=True)
