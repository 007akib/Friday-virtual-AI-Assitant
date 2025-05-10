# # Fix threading and timeout issues in the adaptive response function
# def generate_adaptive_response(query, chat_history=None):
#     # First check if we have a cached response
#     cached_response = get_cached_response(query)
#     if cached_response:
#         return cached_response
    
#     # Determine whether to use online or offline mode
#     use_online = should_use_online_mode(query)
    
#     if use_online:
#         # Try online mode first
#         try:
#             print("Using online mode...")
#             result = None
#             error = None
#             online_completed = False
            
#             def fetch_online():
#                 nonlocal result, error, online_completed
#                 try:
#                     if chat_history and len(chat_history) > 0:
#                         result = send_request2(chat_history)
#                     else:
#                         result = send_request(query)
#                     online_completed = True
#                 except Exception as e:
#                     error = e
#                     online_completed = True
            
#             # Run in thread with timeout
#             thread = threading.Thread(target=fetch_online)
#             thread.daemon = True
#             thread.start()
            
#             # Wait for the thread to complete or timeout
#             thread.join(API_TIMEOUT)
            
#             # If we have an error or timeout, switch to offline mode
#             if error or not online_completed:
#                 if error:
#                     print(f"Error in online mode: {error}")
#                 else:
#                     print("Online response timed out, trying offline mode")
#                 return generate_local_response(query, chat_history)
            
#             if result:
#                 # Cache successful online response
#                 if len(response_cache) >= CACHE_SIZE:
#                     response_cache.pop(next(iter(response_cache)))
#                 response_cache[query] = result
#                 save_cache()
#                 return result
#             else:
#                 print("Online response failed, trying offline mode")
#                 return generate_local_response(query, chat_history)
        
#         except Exception as e:
#             print(f"Exception in online mode: {e}")
#             # Fall back to offline mode
#             try:
#                 return generate_local_response(query, chat_history)
#             except Exception as offline_error:
#                 print(f"Offline mode also failed: {offline_error}")
#                 return random.choice(FALLBACK_MESSAGES)
#     else:
#         # Use offline mode
#         try:
#             print("Using offline mode...")
#             return generate_local_response(query, chat_history)
#         except Exception as e:
#             print(f"Error in offline mode: {e}")
            
#             # If offline fails and we're online, try online as last resort
#             if check_internet(force_check=True):
#                 try:
#                     print("Falling back to online mode after offline failure")
#                     if chat_history and len(chat_history) > 0:
#                         return send_request2(chat_history)
#                     else:
#                         return send_request(query)
#                 except Exception as online_fallback_error:
#                     print(f"Online fallback also failed: {online_fallback_error}")
            
#             return random.choice(FALLBACK_MESSAGES)

# # Fixed local response generation to handle model switching correctly
# def generate_local_response(query, chat_history=None):
#     global CURRENT_MODEL_INDEX
    
#     # Get best available model
#     model_name = get_best_local_model()
    
#     if not model_name:
#         return "I'm having trouble accessing my offline capabilities. Please check that Ollama is running."
    
#     try:
#         # Format the prompt based on chat history
#         if chat_history and len(chat_history) > 0:
#             # Format the chat history for Ollama
#             prompt = ""
#             for message in chat_history[-5:]:  # Only use last 5 messages to keep context window manageable
#                 role = message["role"]
#                 content = message["content"]
#                 if role == "user":
#                     prompt += f"Human: {content}\n"
#                 elif role == "assistant":
#                     prompt += f"Assistant: {content}\n"
            
#             # Add the current query if not already in chat history
#             if chat_history[-1]["role"] != "user" or chat_history[-1]["content"] != query:
#                 prompt += f"Human: {query}\nAssistant:"
#         else:
#             prompt = f"Human: {query}\nAssistant:"
        
#         # Make request to Ollama API
#         response = requests.post(
#             f"{OLLAMA_URL}/generate",
#             json={
#                 "model": model_name,
#                 "prompt": prompt,
#                 "stream": False,
#                 "options": {
#                     "temperature": 0.7,
#                     "top_p": 0.9,
#                     "num_predict": 1024,
#                 }
#             },
#             timeout=OLLAMA_TIMEOUT
#         )
        
#         if response.status_code == 200:
#             result = response.json()
#             answer = result.get("response", "").strip()
            
#             # Mark model as working
#             for model in OLLAMA_MODELS:
#                 if model["name"] == model_name:
#                     model["working"] = True
            
#             # Cache the response for future use
#             if len(response_cache) >= CACHE_SIZE:
#                 # Remove oldest item if cache is full
#                 response_cache.pop(next(iter(response_cache)))
#             response_cache[query] = answer
#             save_cache()
            
#             return answer
#         else:
#             # Mark model as not working
#             for model in OLLAMA_MODELS:
#                 if model["name"] == model_name:
#                     model["working"] = False
            
#             # Try next model
#             CURRENT_MODEL_INDEX = (CURRENT_MODEL_INDEX + 1) % len(OLLAMA_MODELS)
            
#             return random.choice(FALLBACK_MESSAGES)
        
#     except Exception as e:
#         print(f"Error generating local response with {model_name}: {e}")
        
#         # Mark model as not working
#         for model in OLLAMA_MODELS:
#             if model["name"] == model_name:
#                 model["working"] = False
        
#         # Try next model
#         CURRENT_MODEL_INDEX = (CURRENT_MODEL_INDEX + 1) % len(OLLAMA_MODELS)
        
#         return "I encountered an error processing your request offline. Let me try a different approach next time."

# # Update model configuration to include your required deepseek model
# OLLAMA_MODELS = [
#     {"name": "deepseek-coder:1.5b", "installed": False, "working": False},
#     {"name": "phi3:mini", "installed": False, "working": False},
#     {"name": "gemma:2b", "installed": False, "working": False},
#     {"name": "mistral:7b-instruct-v0.2-q4_0", "installed": False, "working": False}
# ]

# # Improved send_request functions with better error handling
# def send_request(query):
#     try:
#         messages = [
#             {"role": "user", "content": query},
#             {"role": "assistant", "content": "```python\n", "prefix": True}
#         ]
        
#         completion = client.chat.completions.create(
#             model="deepseek/deepseek-v3-base:free",
#             messages=messages,
#             stop=["```"],
#             timeout=API_TIMEOUT  # Add timeout parameter
#         )

#         return completion.choices[0].message.content
#     except Exception as e:
#         print(f"Error in send_request: {e}")
#         raise

# def send_request2(messages):
#     try:
#         completion = client.chat.completions.create(
#             model="deepseek/deepseek-v3-base:free",
#             messages=messages,
#             stop=["```"],
#             timeout=API_TIMEOUT  # Add timeout parameter
#         )

#         return completion.choices[0].message.content
#     except Exception as e:
#         print(f"Error in send_request2: {e}")
#         raise

# # Improved check_internet function with better reliability
# def check_internet(force_check=False):
#     global last_online_check, is_online
    
#     # Use cached result if checked recently (within last 10 seconds)
#     current_time = time.time()
#     if not force_check and current_time - last_online_check < 10:
#         return is_online
    
#     # Perform actual check
#     try:
#         # Try multiple reliable endpoints
#         for endpoint in ["8.8.8.8", "1.1.1.1", "208.67.222.222"]:
#             try:
#                 socket.create_connection((endpoint, 53), timeout=2)
#                 is_online = True
#                 last_online_check = current_time
#                 return True
#             except:
#                 continue
        
#         # If all DNS checks fail, try HTTP
#         try:
#             response = requests.get("https://www.google.com", timeout=3)
#             is_online = response.status_code == 200
#         except:
#             is_online = False
#     except:
#         is_online = False
    
#     last_online_check = current_time
#     return is_online