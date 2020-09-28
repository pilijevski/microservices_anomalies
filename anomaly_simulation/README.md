### Adding new anomalies
1. Create new class in anomalies folder as a separate file.
2. Inherit either __Anomaly__ or __PumbaAnomaly__ class.
3. Implement the anomaly <br>
    3.1 If it's a pumba anomaly, only specify the pumba_command in \_\_init\_\_<br>
    3.2 All other anomalies must implement the run_anomaly() method.
3. Import the class in __anomalies/\_\_init\_\_.py__
4. Add key->value pair to __anomaly_dict__ in __anomalies/\_\_init\_\_.py__




### Simulation Config file
