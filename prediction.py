# 不可以刪
def make_predictions(best_model, reference_image_dir, output_dir):
    # Load the YOLO model using the provided model path
    model = best_model

    # Call the predict method with the correct argument format
    return model.predict(reference_image_dir, save=True, project=output_dir, classes=[5])
