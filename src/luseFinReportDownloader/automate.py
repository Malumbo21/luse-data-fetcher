import io
import download
import read_data
import pandas as pd
import tempfile

# Create a downloader object from the Downloader class
downloader = download.Downloader()

# Call fetch_streams of the downloader object
downloader.fetch_streams()

# Assign downloader.streams to a variable
streams = downloader.streams

# Iterate over the streams
for idx, stream in enumerate(streams):
    # Create a temporary file to save the stream
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf_file:
        temp_pdf_file.write(stream.getvalue())
        src_pdf = temp_pdf_file.name
    
    # Call read_data function from the read_data module with the source PDF
    dataframe = read_data.read_data(src_pdf)
    
    # Save the dataframe with a unique name
    output_filename = f"output_data_{idx}.csv"
    dataframe.to_csv(output_filename, index=False)
    
    # Clean up: Remove the temporary PDF file
    temp_pdf_file.close()

print("Data processing and saving complete.")
