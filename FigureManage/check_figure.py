import ctypes


def check_figure(widget, next_time=1500):
    '''
    检测是否有指纹按压在指纹仪上，如果有，则采集，然后发出指纹按压信号
    :param next_time: 有指纹仪时采集频率
    :return:
    '''
    try:
        f = widget.figure_dll.FPICheckFinger(widget.parent.device.figure)
        if f == 0:
            widget.parent.device.figure_timer.stop()
            pstz = ctypes.create_string_buffer(512)
            length = ctypes.create_string_buffer(512)
            widget.figure_dll.FPIFeatureWithoutUI(0, pstz, length)
            widget.figure_checked.emit(pstz.raw)
            del pstz, length
            widget.parent.device.figure_timer.start(next_time)
        elif f == 1:
            pass
    except BaseException:
        widget.parent.warn.add_warn('指纹采集出错')
