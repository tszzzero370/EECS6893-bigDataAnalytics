Two MLP classiifers for final_status and final_months prediction.
# Reload
model_months = tf.keras.models.load_model('model_months')
# Check architecture
model_months.summary()
