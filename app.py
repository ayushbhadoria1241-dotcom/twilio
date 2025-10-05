from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route('/')
def home():
    return "Twilio TwiML Server is running!"

@app.route('/airflow-alert', methods=['GET', 'POST'])
def airflow_alert():
    # Get parameters from URL query string (GET) or form data (POST)
    dag_id = request.values.get('dag_id', 'unknown DAG')
    task_id = request.values.get('task_id', 'unknown task')
    state = request.values.get('state', 'failed')
    
    # Clean up underscores for better speech
    dag_id_spoken = dag_id.replace('_', ' ')
    task_id_spoken = task_id.replace('_', ' ')
    
    # Create TwiML response
    response = VoiceResponse()
    
    # Attention getter
    response.say(
        "Attention! This is a critical alert from Grafana.",
        voice='alice',
        language='en-US'
    )
    response.pause(length=1)
    
    # Main alert with details
    message = (
        f"An Airflow task has failed. "
        f"The DAG name is {dag_id_spoken}. "
        f"The task name is {task_id_spoken}. "
        f"Current status is {state}. "
        f"Please check your monitoring dashboard immediately."
    )
    
    response.say(message, voice='alice', language='en-US')
    response.pause(length=2)
    
    # Repeat key info
    response.say(
        f"I repeat, task {task_id_spoken} in DAG {dag_id_spoken} has failed.",
        voice='alice',
        language='en-US'
    )
    response.pause(length=1)
    
    # Instructions
    response.say(
        "Check Microsoft Teams for full details, or login to Grafana dashboard.",
        voice='alice',
        language='en-US'
    )
    response.pause(length=1)
    
    # Closing
    response.say(
        "This is an automated alert from A 360 data platform team. Thank you.",
        voice='alice',
        language='en-US'
    )
    
    return str(response), 200, {'Content-Type': 'text/xml'}

@app.route('/test-twiml', methods=['GET', 'POST'])
def test_twiml():
    """Test endpoint to see what TwiML is generated"""
    # Get parameters from either query string (GET) or form data (POST)
    dag_id = request.values.get('dag_id', 'test_dag')
    task_id = request.values.get('task_id', 'test_task')
    state = request.values.get('state', 'failed')
    
    dag_id_spoken = dag_id.replace('_', ' ')
    task_id_spoken = task_id.replace('_', ' ')
    
    response = VoiceResponse()
    response.say(
        "Attention! This is a critical alert from Airflow.",
        voice='alice',
        language='en-US'
    )
    response.pause(length=1)
    
    message = (
        f"An Airflow task has failed. "
        f"The DAG name is {dag_id_spoken}. "
        f"The task name is {task_id_spoken}. "
        f"Current status is {state}. "
        f"Please check your monitoring dashboard immediately."
    )
    
    response.say(message, voice='alice', language='en-US')
    
    return str(response), 200, {'Content-Type': 'text/xml'}

if __name__ == '__main__':
    import sys
    print("=" * 50, flush=True)
    print("Twilio TwiML Server Starting...", flush=True)
    print("=" * 50, flush=True)
    print("Server will run on: http://localhost:5001", flush=True)
    print("Test endpoint: http://localhost:5001/test-twiml?dag_id=my_dag&task_id=my_task", flush=True)
    print("=" * 50, flush=True)
    sys.stdout.flush()
    app.run(host='0.0.0.0', port=5001, debug=True)