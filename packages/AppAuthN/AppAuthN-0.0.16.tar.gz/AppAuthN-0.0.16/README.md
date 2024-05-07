# AppAuthN

`AppAuthN` 是一個用於驗證 xApp 身份的 Python 模塊。

## 使用方法

1. download package:

    ```bash
   pip install AppAuthN
    
2. 進行註冊

    ```python
    #模型
    import AppAuthN.CertificationReceiver as register
    register_api = <url>
    inference_api = <url>
    register.kongapi(register_api, inference_api)

    register_data = {
        "application_uid": <application_uid>,
        "application_token": <application_token>,
        "position_uid": <position_uid>,
        "inference_client_name": <inference_client_name>,
    }
    register.send_register_request(register_data)

3. 進行推論：

   ```python
    #模型
    import AppAuthN.InferenceResult as infer
    raw_data = {
        "application_uid": <application_uid>,
        "position_uid": <position_uid>,
        "inference_client_name": <inference_client_name>,
        "value": <value>
    }
    inference.send_rawdata(raw_data)

# 注意事项

-請確保提供有效的输入，否則驗證可能會失败。
