$(document).ready(function() {
    // 输入框
    var textarea = document.querySelector('.resize-none');
    textarea.addEventListener('input', adjustHeight);

    function adjustHeight() {
        this.style.height = '38px';
        var maxHeight = 114;
        if (this.scrollHeight <= maxHeight) {
            this.style.height = `${this.scrollHeight}px`;
        } else {
            this.style.height = `${maxHeight}px`;
        }
    }

    // 聊天界面显示消息
    function displayMessage(message, align) {
        message = message.replace(/\n/g, '<br>');
        let messageAlign = (align === 'assistant') ? 'justify-content-start' : 'justify-content-end';
        let messageBox = '<div class="d-flex ' + messageAlign + '"><div class="bg-light p-2 rounded mt-1 mb-1 message-box"><p class="mb-0">' + message + '</p></div></div>';
        if (align === 'user') {
            messageBox = '<div class="d-flex ' + messageAlign + '"><div class="bg-primary text-white p-2 rounded mt-1 mb-1 message-box"><p class="mb-0">' + message + '</p></div></div>';
        }
        $('.card-body').append(messageBox); // 将消息添加到聊天界面
        // 滚动到最新消息
        $('.chat-container').scrollTop($('.chat-container')[0].scrollHeight);
    }

    function setupEventSource() {
        // 关闭旧的 EventSource 如果存在
        if (window.eventSource) {
            window.eventSource.close();
        }

        window.eventSource = new EventSource('/update');

        window.eventSource.onmessage = function(event) {
            let lastDiv = $('.bg-light.p-2.rounded.mt-1.mb-1.message-box').last();
            let pTag = lastDiv.find('p');
            pTag[0].innerHTML += event.data;
            // 滚动到聊天容器的底部以确保最新消息可见
            $('.chat-container').scrollTop($('.chat-container')[0].scrollHeight);
        };

        window.eventSource.onerror = function(event) {
            window.eventSource.onerror = function(event) {
                console.log('EventSource failed:', event);
                window.eventSource.close();
                setTimeout(setupEventSource, 5000); // 设置5秒后重连
            };
        };

        window.eventSource.addEventListener('start', function(event) {
            console.log(event)
            let lastDiv = $('.bg-light.p-2.rounded.mt-1.mb-1.message-box').last();
            let pTag = lastDiv.find('p');
            pTag[0].innerHTML = '';
        });

        window.eventSource.addEventListener('end', function(event) {
            let lastDiv = $('.bg-light.p-2.rounded.mt-1.mb-1.message-box').last();
            let pTag = lastDiv.find('p');
            let message = pTag[0].innerHTML;

            $.ajax({
                url: '/response_commit',  // 确保 URL 是正确的
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ content: message }),
                success: function() {
                    $('button').prop('disabled', false);
                    window.eventSource.close()
                },
                error: function(error) {
                    console.log('Error fetching the session messages:', error);
                }
            });
        });
    }

    // setupEventSource(); // 初始化 SSE 连接

    // 当发送按钮被点击
    $('button').click(function() {
        $('button').prop('disabled', true);
        var message = $('textarea').val();
        if (message.trim() !== '') {
            displayMessage(message, 'user');  // 显示用户消息
            $('textarea').val('');  // 清空输入区域
            textarea.style.height = '38px';  // 重置输入区域高度

            setupEventSource()

            // 发送消息到服务器并获取响应
            $.ajax({
                url: '/chat-stream',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ content: message }),
                success: function() {
                    // 假设响应是一个简单的字符串
                    displayMessage('...', 'assistant');
                },
                error: function() {
                    displayMessage('Sorry, there was an error.', 'assistant');
                }
            });
        }
    });

    $.ajax({
        url: '/session/10001',  // 确保 URL 是正确的
        type: 'GET',
        success: function(data) {
            data.forEach(msg => {
                displayMessage(msg.content, msg.role)
            });
        },
        error: function(error) {
            console.log('Error fetching the session messages:', error);
        }
    });

});
