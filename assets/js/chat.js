$(document).ready(function() {
    // 全局变量锁
    var lock = false;
    var imageNext = false;
    var tempText = '';
    var tempImage = '';

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
    function displayMessage(message, align, type) {
        $('.empty-div').remove();

        let messageBox
        if(type === 'text'){
            message = message.replace(/\n/g, '<br>');
            let messageAlign = (align === 'assistant') ? 'justify-content-start' : 'justify-content-end';
            messageBox = '<div class="d-flex ' + messageAlign + '"><div class="bg-light p-2 rounded mt-1 mb-1 message-box"><p class="mb-0">' + message + '</p></div></div>';
            if (align === 'user') {
                messageBox = '<div class="d-flex ' + messageAlign + '"><div class="bg-primary text-white p-2 rounded mt-1 mb-1 message-box"><p class="mb-0">' + message + '</p></div></div>';
            }

        }else {
            messageBox = '<div class="d-flex justify-content-start"><div class="bg-light p-2 rounded mt-1 mb-1 message-box"><p class="mb-0"><img alt="image" src="' + message + '"></p></div></div>';
        }
        $('.card-body.chat-container').append(messageBox); // 将消息添加到聊天界面

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
            if(imageNext){
                let lastDiv = $('.bg-light.p-2.rounded.mt-1.mb-1.message-box').last();
                lastDiv.remove();
                imageNext = false;
                tempImage = event.data;
                displayMessage(tempImage, 'assistant', 'image')
            }else {
                tempText += event.data;
                let lastDiv = $('.bg-light.p-2.rounded.mt-1.mb-1.message-box').last();
                let pTag = lastDiv.find('p');
                pTag[0].innerHTML += event.data;
            }
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
            let lastDiv = $('.bg-light.p-2.rounded.mt-1.mb-1.message-box').last();
            let pTag = lastDiv.find('p');
            pTag[0].innerHTML = '';
        });

        window.eventSource.addEventListener('end', function(event) {
            $.ajax({
                url: '/response_commit',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ content: tempText }),
                success: function() {
                    tempText = '';
                    lock = false;
                    $('button').prop('disabled', false);
                    window.eventSource.close()
                },
                error: function(error) {
                    console.log('Error fetching the session messages:', error);
                }
            });
        });

        window.eventSource.addEventListener('image', function(event) {
            imageNext = true;
        });

        window.eventSource.addEventListener('end-image', function(event) {
            $.ajax({
                url: '/image_commit',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ content: tempImage }),
                success: function() {
                    tempImage = '';
                    lock = false;
                    $('button').prop('disabled', false);
                    window.eventSource.close()
                },
                error: function(error) {
                    console.log('Error fetching the session messages:', error);
                }
            });
        });
    }

    // 当发送按钮被点击
    $('button').click(function() {
        if (lock) { return; }

        var message = $('textarea').val();
        if (message.trim() !== '') {
            lock = true;
            $('button').prop('disabled', true);

            displayMessage(message, 'user', 'text');  // 显示用户消息
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
                    displayMessage('...', 'assistant', 'text');
                },
                error: function() {
                    displayMessage('Sorry, there was an error.', 'assistant', 'text');
                }
            });
        }
    });

    //session
    // 双击修改Session Info
    $('#sessionList').on('dblclick', '.session', function() {
        if (lock) { return; }

        let $this = $(this)
        let currentText = $(this).text();
        let input = $('<input>', {
            type: 'text',
            value: currentText,
            blur: function() {
                let newText = $(this).val().trim();
                if (newText === '') {
                    newText = currentText;
                }else {
                    //同步到数据库
                    let url = '/session/' + $this.attr('data-session-id') + '/' + newText
                    $.ajax({
                        url: url,
                        type: 'PUT',
                        success: function () {},
                        error: function(error) {
                            console.log('Error update the session:', error);
                        }
                    });
                }
                $(this).replaceWith($('<span>').text(newText));
            },
            keypress: function(e) {
                if (e.which === 13) {  // 按 Enter 键
                    $(this).blur();
                }
            }
        });

        $(this).html(input);
        input.focus();
    });

    // delete session
    let deleteBtn = $('#deleteBtn');
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance($('#liveToast'))

    // 单击选中session
    $('#sessionList').on('click', '.session', function() {
        if (lock) { return; }

        $this = $(this)
        $('.session').removeClass('selected');
        $this.addClass('selected');
        let session_id = $this.attr('data-session-id');

        // 定位删除按钮
        let pos = $(this).position();
        deleteBtn.css({
            top: pos.top + $(this).outerHeight() - deleteBtn.outerHeight() - 6,
            display: 'flex'
        });
        // 绑定删除事件
        $('#confirmDelete').off('click').on('click', () => {
            $.ajax({
                url: '/session/' + session_id,
                type: 'DELETE',
                success: function () {
                    $this.remove();
                    deleteBtn.hide();
                    toastBootstrap.show();
                    let session = $('#sessionList .session:first');
                    if(session){
                        displaySession(session.attr('data-session-id'));
                        session.addClass('selected');
                    }
                },
                error: function(error) {
                    console.log('Error delete the session:', error);
                }
            });
        });

        //渲染对应session
        $('.chat-container').empty();
        displaySession(session_id);
    });

    // 获取全部Session
    $.ajax({
        url: '/sessions',
        type: 'GET',
        success: function (data){
            data.forEach(session => {
                let sessionHTML = '<li class="list-group-item session" data-session-id="' + session.session_id + '">'
                    + session.session_info + '</li>';
                $('#sessionList').append(sessionHTML)
            });
            if (data.length > 0) {
                displaySession(data[0].session_id);
                $('#sessionList .session:first').addClass('selected');
            }
        },
        error: function(error) {
            console.log('Error fetching the sessions:', error);
        }
    });

    // new session
    $('#newSession').on('click',function (){
        if (lock) { return; }

        $.ajax({
            url: '/session',
            type: 'POST',
            success: function (data){
                deleteBtn.hide();
                let sessionHTML = '<li class="list-group-item session" data-session-id="' + data.session_id + '">new session</li>';
                $('#sessionList').prepend(sessionHTML);
                $('.session').removeClass('selected');
                $('#sessionList .session:first').addClass('selected');
                $('.chat-container').html('<div class="empty-div"><h3>Empty Session</h3></div>')
            },
            error: function(error) {
                console.log('Error add the session:', error);
            }
        });
    });

    // 渲染Session内容
    function displaySession(id) {
        let url = '/session/' + id
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                if(data.length === 0){
                    $('.chat-container').html('<div class="empty-div"><h3>Empty Session</h3></div>')
                }
                data.forEach(msg => {
                    displayMessage(msg.content, msg.role, msg.type)
                });
            },
            error: function(error) {
                console.log('Error fetching the session messages:', error);
            }
        });
    }
});
