# Socket Demo: 增强聊天应用

[English version](README.md)

#### 介绍
本项目展示了一个高级聊天应用，集成了第三方AI聊天接口进行对话。系统支持持久连接以实现流式对话，并采用复杂的数据结构来存储对话历史和上下文信息。本指南详细介绍了项目运行所需的设置步骤。

#### 特点
- **第三方AI聊天集成**：利用第三方AI实现实时的块状对话。
- **长连接通信**：实施持久连接技术，确保对话的连续性和流畅性。
- **上下文管理**：采用算法处理和管理上下文信息，使对话更加连贯和具有上下文感知。
- **交互式前端**：一个用户友好的界面，允许用户参与对话，这些对话与后端的长连接通信技术互动。
- **扩展的UI功能**：支持同时存储多个对话历史，增强用户互动。
- **多对话的后端逻辑**：调整后端逻辑，有效关联并切换多个对话。
- **集成绘图API**：集成第三方绘图API，修改后端逻辑以识别和处理绘图任务，并将绘图结果作为图像文件保存在本地服务器。
- **结果呈现**：将绘图结果以图像文件的形式返回给用户。

#### 技术栈
- **Flask**：一个轻量级且灵活的Python Web开发微框架，用于处理后端逻辑和路由。
- **Bootstrap**：一个前端框架，用于创建现代且响应式的布局，确保应用在不同设备上既美观又实用。
- **服务器发送事件（SSE）**：用于处理客户端和服务器之间实时双向通信，对于维护实时聊天会话的长连接至关重要。
- **ChatGPT**：作为AI引擎集成，以驱动基于上下文和之前互动的对话能力。
- **DALL-E**：用于根据聊天中的文本描述生成图像，通过提供视觉反馈增强交互体验的第三方API。

#### 安装和设置指南

要成功安装并运行此项目，请按照以下步骤操作：

1. **安装依赖**：
   首先，确保安装 `requirements.txt` 中列出的所有依赖项。打开终端或命令提示符，导航至项目根目录，并运行以下命令：
   ```bash
   pip install -r requirements.txt
   ```

2. **配置数据库**:
   接下来，执行 `data.sql` 脚本以建立数据库架构。该脚本将创建必要的表和初始数据。之后，请根据您的数据库配置修改 `routes.__init__.py` 中的数据库设置。

3. **设置环境变量**:
   最后，在项目根目录创建一个 .env 文件，其中包含用于存储您的 OpenAI API 密钥的关键环境变量。内容应如下所示：
   ```
   OPENAI_API_KEY=your_api_key
   ACCESS_KEY_ID=your_aliyun_id
   ACCESS_KEY_SECRET=your_aliyun_secret
   ```

完成设置步骤后，您应该能够运行项目并开始测试其套接字通信和AI集成聊天功能。如遇任何问题，请确保每个步骤都已正确配置和执行。