TRANSLATIONS = {
    "en": {
        "page_title": "Legal Document Chatbot",
        "title": "⚖️ Legal Document Q&A Chatbot",
        "description": "Upload your PDFs, Word documents, or provide web URLs to start asking questions!",
        "config_header": "⚙️ Configuration",
        "api_key_label": "Google Gemini API Key",
        "api_key_placeholder": "Paste your API key here",
        "api_key_info": "💡 To use this app, please enter your own Google Gemini API Key. You can get a free one from [Google AI Studio](https://aistudio.google.com/app/apikey).",
        "admin_header": "🔒 Admin Access",
        "admin_password_label": "Admin Password",
        "admin_success": "✅ Admin Access Granted",
        "upload_header": "📄 Upload Data Sources",
        "upload_label": "Upload Documents (PDF, DOCX)",
        "urls_label": "Web URLs (one per line)",
        "urls_placeholder": "https://example.com/legal-document",
        "process_btn": "🚀 Process Documents",
        "admin_info": "Log in as Admin to upload new documents.",
        "how_to_use_header": "### How to use:",
        "how_to_use_steps": "1. Enter your Google Gemini API Key.\n2. Upload your documents or enter URLs.\n3. Click 'Process Documents'.\n4. Ask questions in the chat!",
        "error_api_key": "⚠️ Please provide a Google API Key.",
        "spinner_loading": "⏳ Loading documents...",
        "error_doc_format": "❌ '{file_name}' is a .doc file. Please convert it to .docx first.",
        "error_loading": "❌ Error loading {file_name}: {error}",
        "warning_no_docs": "⚠️ No documents loaded. Please upload files or provide valid URLs.",
        "spinner_indexing": "🧠 Processing and indexing documents...",
        "success_processed": "✅ Documents processed successfully!",
        "error_processing": "❌ Error during processing: {error}",
        "chat_header": "### 💬 Chat",
        "view_sources": "📚 View Sources",
        "source_label": "**Source {index}:**",
        "chat_placeholder": "Ask a question about the provided documents...",
        "warning_no_docs_uploaded": "⚠️ No documents have been uploaded yet. An admin must upload documents first.",
        "error_api_key_sidebar": "⚠️ Please provide a Google API Key in the sidebar.",
        "thinking": "Thinking...",
        "error_general": "❌ An error occurred: {error}",
        "system_prompt": (
            "You are an expert legal assistant specialized in analyzing documents and answering questions based on them. "
            "Use the following pieces of retrieved context to answer the user's question accurately. "
            "If the answer cannot be found in the provided context, state clearly that you don't know based on the provided documents. "
            "Do not make up information. Provide a clear and well-structured answer."
            "\n\n"
            "Context:\n{context}"
        )
    },
    "vi": {
        "page_title": "Chatbot Văn bản Pháp luật",
        "title": "⚖️ Chatbot Hỏi đáp Văn bản Pháp luật",
        "description": "Tải lên tệp PDF, Word hoặc cung cấp URL web để bắt đầu đặt câu hỏi!",
        "config_header": "⚙️ Cấu hình",
        "api_key_label": "Mã API Google Gemini",
        "api_key_placeholder": "Dán mã API của bạn tại đây",
        "api_key_info": "💡 Để sử dụng ứng dụng này, vui lòng nhập Mã API Google Gemini của bạn. Bạn có thể nhận mã miễn phí từ [Google AI Studio](https://aistudio.google.com/app/apikey).",
        "admin_header": "🔒 Truy cập Quản trị",
        "admin_password_label": "Mật khẩu Quản trị",
        "admin_success": "✅ Đã cấp quyền Quản trị",
        "upload_header": "📄 Tải lên Nguồn Dữ liệu",
        "upload_label": "Tải lên Tài liệu (PDF, DOCX)",
        "urls_label": "URL Web (mỗi dòng một URL)",
        "urls_placeholder": "https://example.com/tai-lieu-phap-luat",
        "process_btn": "🚀 Xử lý Tài liệu",
        "admin_info": "Đăng nhập với tư cách Quản trị viên để tải lên tài liệu mới.",
        "how_to_use_header": "### Hướng dẫn sử dụng:",
        "how_to_use_steps": "1. Nhập Mã API Google Gemini của bạn.\n2. Tải lên tài liệu hoặc nhập URL.\n3. Nhấp vào 'Xử lý Tài liệu'.\n4. Đặt câu hỏi trong ô chat!",
        "error_api_key": "⚠️ Vui lòng cung cấp Mã API Google.",
        "spinner_loading": "⏳ Đang tải tài liệu...",
        "error_doc_format": "❌ '{file_name}' là tệp .doc. Vui lòng chuyển sang .docx trước.",
        "error_loading": "❌ Lỗi khi tải {file_name}: {error}",
        "warning_no_docs": "⚠️ Không có tài liệu nào được tải. Vui lòng tải lên tệp hoặc cung cấp URL hợp lệ.",
        "spinner_indexing": "🧠 Đang xử lý và lập chỉ mục tài liệu...",
        "success_processed": "✅ Tài liệu đã được xử lý thành công!",
        "error_processing": "❌ Lỗi trong quá trình xử lý: {error}",
        "chat_header": "### 💬 Trò chuyện",
        "view_sources": "📚 Xem Nguồn",
        "source_label": "**Nguồn {index}:**",
        "chat_placeholder": "Đặt câu hỏi về các tài liệu đã cung cấp...",
        "warning_no_docs_uploaded": "⚠️ Chưa có tài liệu nào được tải lên. Quản trị viên phải tải tài liệu lên trước.",
        "error_api_key_sidebar": "⚠️ Vui lòng cung cấp Mã API Google ở thanh bên.",
        "thinking": "Đang suy nghĩ...",
        "error_general": "❌ Đã xảy ra lỗi: {error}",
        "system_prompt": (
            "Bạn là một chuyên gia trợ lý pháp lý chuyên phân tích tài liệu và trả lời các câu hỏi dựa trên chúng. "
            "Sử dụng các mẩu ngữ cảnh đã được truy xuất sau đây để trả lời câu hỏi của người dùng một cách chính xác. "
            "Nếu câu trả lời không thể tìm thấy trong ngữ cảnh được cung cấp, hãy nêu rõ rằng bạn không biết dựa trên các tài liệu được cung cấp. "
            "Không tự tạo ra thông tin. Cung cấp một câu trả lời rõ ràng và có cấu trúc tốt."
            "\n\n"
            "Ngữ cảnh:\n{context}"
        )
    }
}
