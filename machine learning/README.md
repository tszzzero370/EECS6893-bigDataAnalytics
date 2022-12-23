Two MLP classiifers for final_status and final_months prediction.
The models are contrructed under TF 2.6.0, and can be loaded with any TF version higher than 2.6.0.
# Reload
model_months = tf.keras.models.load_model('model_months')
# Check architecture
model_months.summary()
