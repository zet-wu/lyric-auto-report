"""Render current module reports from completed, independently scored results."""
from pathlib import Path
import argparse, json, statistics, sys, csv
sys.path.insert(0,str(Path(__file__).resolve().parent/'timing'))
from separator_registry import MODELS

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((ROOT / 'results' / name).read_text())
def write(name, lines):
    (ROOT / 'reports' / name).write_text('\n\n'.join(lines) + '\n')
def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                     '| ' + ' | '.join(['---'] * len(headers)) + ' |',
                     *['| ' + ' | '.join(map(str, row)) + ' |' for row in rows]])
def metric_table(rows):
    return table(['条件', '分母', '100 ms 命中', '200 ms 命中', '起／止 MAE ms',
                  '起／止绝对误差 P95 ms', '缺失', '>1 秒'],
                 [[name, r['n'], f"{r['hit100']}（{r['hit100_pct']:.2f}%）",
                   f"{r['hit200']}（{r['hit200_pct']:.2f}%）",
                   f"{r['start_mae_ms']:.2f} / {r['end_mae_ms']:.2f}",
                   f"{r['start_abs_p95_ms']:.2f} / {r['end_abs_p95_ms']:.2f}",
                   r['missing_or_nonpositive'], r['over_1s']] for name, r in rows])

def summarize(rows):
    errors = [[1000*(p-g) for p,g in zip(r['prediction'],r['reference'])] for r in rows
              if r['prediction'] is not None and r['prediction'][1] > r['prediction'][0]]
    def p95(values):
        values = sorted(values)
        k = .95*(len(values)-1)
        lo = int(k)
        return values[lo]+(values[min(lo+1,len(values)-1)]-values[lo])*(k-lo)
    n = len(rows)
    result = {'n': n, 'missing_or_nonpositive': n-len(errors),
              'over_1s': sum(max(map(abs,e)) > 1000 for e in errors)}
    for limit in (100,200):
        result[f'hit{limit}'] = sum(max(map(abs,e)) <= limit+1e-6 for e in errors)
        result[f'hit{limit}_pct'] = 100*result[f'hit{limit}']/n
    for i,name in enumerate(('start','end')):
        values = [abs(e[i]) for e in errors]
        result[f'{name}_mae_ms'] = sum(values)/len(values) if values else float('nan')
        result[f'{name}_abs_p95_ms'] = p95(values) if values else float('nan')
    return result

DEFINITIONS = ('双端命中要求起点和终点同时在阈值内。MAE（Mean Absolute Error，平均绝对误差）'
               '为有效端点与参考之差的绝对值均值；P95 是绝对误差的第 95 百分位数。'
               '缺失或无效单元保留在命中率分母，MAE 与 P95 只计算有效端点。'
               '任一端点绝对误差超过 1 秒即记为大误差项。')
CORE = ('core 指人声活动检测保留的核心区间，拼接时删去区间之间的音频，'
        '对齐后映射回原曲；带缓冲拼接在保留区间两侧增加上下文。'
        'CTC（Connectionist Temporal Classification，连接时序分类）'
        '在本实验中用于从逐帧发音标签概率解码已知读音的时间边界。')

def timing():
    primary = {f's{i:02}' for i in range(1,11)} | {'s12','s15'}
    rows = [r for r in read('timing/scored-units.json') if r['song'] in primary and r['language'] == 'ja']
    groups = [('Lazulite Studio 人工读音投影', [r for r in rows if r['method'] == 'studio_surface' and r['comparison'] == 'untimed'])]
    modes = {'untimed': '无时间正文＋Demucs', 'trusted': '人工行时间＋Demucs', 'lead_untimed': '无时间正文＋BS Karaoke'}
    for mode,label in modes.items():
        groups.append(('Timing／'+label,[r for r in rows if r['method'] == 'timing_'+mode]))
    completion = [r for r in read('timing/metrics.json')['completion'] if r['song'] in primary]
    assert len(completion) == 36, 'Incomplete Timing pipeline'
    lines = ['# Timing 完整链路与细对齐诊断',
             '本轮使用 12 首日语歌曲评价 Timing 的正文自动读音管线，另用人工读音与人工行窗口'
             '诊断细对齐。公平比较各产品人工读音、统一分离与自动读音条件的主结果见'
             '[八路线三组比较](comparison.md)。',
             '完整链路与模块诊断使用固定的共用研究环境（Transformers 4.57.6）；主比较中的 Timing 另在 Transformers 5.15.0 环境复测。两种环境的实测范围分别保存，不能混用指标。',
             '## 正文输入的完整链路',
             '三种条件分别采用无时间正文配 Demucs、可信人工行时间配 Demucs、'
             '以及 BS Karaoke 配无时间正文。可信人工行时间条件属于定位诊断。'
             'Lazulite Studio 此处使用人工 Ruby（附在正文上的读音标注）投影，'
             '与 Timing 的正文自动转换是两种输入形式；表中保留这个工作流差异。',
             DEFINITIONS,
             metric_table([(name,summarize(selected)) for name,selected in groups]),
             table(['Timing 条件','完成歌曲'], [[label, f"{sum(not r.get('error') for r in completion if r['mode']==mode)}/12"] for mode,label in modes.items()]),
             '表格按原正文对象边界计分；失败歌曲保留全部分母。'
             '粗定位占位输出不作为有效细对齐结果。Lazulite Studio 当前产品采用后的原标注细项另见主比较报告。',
             '## 原生失败',
             table(['歌曲','条件','首个阻断错误'],
                   [[r['song'],modes[r['mode']],r['error'].strip().splitlines()[-1].replace('|','／').replace('`','')[:250]]
                    for r in completion if r.get('error')]),
             '完整调用栈与成功输出见[逐曲目录](../results/timing/timing)。'
             '这些失败保留原生行为；输入读音、定位窗口或显示映射的拒绝都会影响完整链路覆盖率。']
    controlled = [r for r in read('timing/controlled-scored-units.json') if r['song'] in primary and r['language']=='ja_en']
    lines += ['## 固定读音与人工窗口',
              '只选可编译的纯假名配对单元，NextFire 与 TIFA 使用相同 Demucs 人声、人工读音和人工行窗口。'
              '这项实验排除了自动读音和粗定位的差异，不能直接代表无人工时间输入的完整流程。',
              metric_table([(m,summarize([r for r in controlled if r['method']==m])) for m in ('nextfire','tifa')])]
    hybrid = [r for r in read('timing/hybrid-scored-units.json') if r['song'] in primary and r['language']=='ja_en']
    lines += ['## 预测窗口内的 TIFA 细化',
              '细化窗口从首轮预测生成；无有效候选或未通过接受检查时保留首轮输出。'
              '实际窗口和采用决定分别保存在协议与指标中。',
              metric_table([(m,summarize([r for r in hybrid if r['method']==m])) for m in ('baseline','hybrid')]),
              '## 复核与语种补测',
              '[完整链路指标](../results/timing/metrics.json)、[共同文本边界](../results/timing/paired-common-units.json)、'
              '[固定窗口指标](../results/timing/controlled-metrics.json)与'
              '[细化采用记录](../results/timing/hybrid-metrics.json)保存本轮结果。'
              '日粤混合与潮汕话标注不进入日语主组。人工窗口下的原生粤语补测见'
              '[粤语指标](../results/timing/yue-native-metrics.json)；英语诊断见'
              '[英语指标](../results/timing/english-metrics.json)。']
    write('timing.md', lines)

def ablation():
    data = read('ablation/metrics.json')
    rows = [r for r in data['aggregate'] if r['cohort'] == 'primary' and r['subset'] == 'all']
    assert rows and all(r['songs'] == 12 for r in rows), 'Incomplete matrix'
    labels = {'concat': 'core 拼接', 'padded': '带缓冲拼接', 'full': '完整人声',
              'auto_mms': '自动 MMS 窗口', 'auto_nf': '自动 NextFire 窗口',
              'human': '人工行窗口', 'auto_mms_pause': 'MMS 窗口＋尾点搜索',
              'fixed_cores': '固定 Demucs core'}
    def metric(r):
        return {**r, 'hit100_pct': 100*r['rate100'], 'hit200_pct': 100*r['rate200'],
                'missing_or_nonpositive': r['missing'], 'over_1s': r['gt1s'],
                'start_abs_p95_ms': r['start_p95_ms'], 'end_abs_p95_ms': r['end_p95_ms']}
    lines = ['# 对齐后端、窗口和人声输入',
             '本轮使用固定人工读音，对 12 首日语歌曲重跑模型、输入窗口和分离器组合。'
             '本报告评价模块条件；当前 Lazulite Studio 的固定路线与 MMS_FA 智能延长输出见'
             '[八路线比较](comparison.md)。模块原始 MMS_FA 与产品智能延长分别计分。',
             CORE, DEFINITIONS,
             '主组使用可配对的纯假名单元，独立长音符并入前一个单元。'
             '宏平均表示先逐曲求命中率，再对歌曲等权平均；下面计数表按所有单元汇总。'
             '人工窗口用于诊断，不代表无人工时间输入的自动化成绩。',
             '![后端与人声输入](../results/ablation/matrix.png)']
    for backend in ('nextfire', 'tifa', 'mms_fa'):
        selected = [r for r in rows if r['backend'] == backend and r['separator'] in ('demucs', 'bs', 'kim')]
        lines += ['## ' + backend, metric_table([(r['separator'] + '／' + labels[r['strategy']], metric(r)) for r in selected])]
    lines += ['## 补充分离器',
              '固定 NextFire，补充 SCNet、DTTNet、BS-RoFormer Viperx、MelBand 和 Windowed。'
              'BS-RoFormer Viperx 与 BS Karaoke 使用不同权重。',
              metric_table([(r['separator'] + '／' + labels[r['strategy']], metric(r)) for r in rows
                            if r['separator'] not in ('demucs', 'bs', 'kim')])]
    gap = [r for r in read('mms-gap-fill/metrics.json') if r['song'] == 'ALL'
           and r['subset'] == 'all' and r['separator'] == 'demucs' and r['strategy'] == 'full']
    lines += ['## 行内空隙填补诊断',
              '对同一行中相邻的两个有效单元，若前一个结束早于后一个开始，则按统一空隙上限'
              '延长前一单元至后一单元起点。不改变起点、重叠、缺失与行末端点。'
              '此规则不等同于 Lazulite Studio 的智能延长；阈值不按歌曲成绩选择。',
              metric_table([(r['variant'], {**r, 'hit100_pct': 100*r['hit100']/r['n'],
                            'hit200_pct': 100*r['hit200']/r['n'], 'missing_or_nonpositive': r['missing']}) for r in gap]),
              '[全部阈值、输入策略及停顿子集](../results/mms-gap-fill/metrics.json)和'
              '[逐项修改](../results/mms-gap-fill/edits.json.gz)保留填补收益与尾点偏晚的代价。',
              '## 复核材料',
              '[协议](../results/ablation/protocol.json)、[完整表](../results/ablation/tables.md)、'
              '[汇总指标](../results/ablation/metrics.json)、[窗口审计](../results/ablation/window-audit.json)、'
              '[独立长音符边界](../results/ablation/standalone-hold-boundaries.json)和'
              '[重复元音探针](../results/ablation/duplicate-vowel-probe.json)保存本轮全部输出。'
              '原始叶级单元与保存路径对照见[分离与对齐](separation-alignment.md)。']
    write('alignment-backends.md', lines)

def separation():
    rows = [r for r in read('separation-alignment/metrics.json')['aggregate'] if r['group'] == 'japanese']
    assert len(rows) == 60 and all(r['songs'] == 12 for r in rows), 'Incomplete separator matrix'
    labels = {'global': '完整人声', 'concat_core': 'core 拼接', 'concat_padded': '带缓冲拼接'}
    write('separation-alignment.md', [
        '# 十种分离配置对歌词对齐的影响',
        '对 12 首日语歌曲使用相同人工读音、NextFire 与标准 CTC，'
        '比较十种分离配置、两条保存路径与三种音频组织方式。下游均使用 GPU 分离结果。' + CORE,
        '浮点路径使用原混音作为活动分析参考；PCM24（24 位音频采样）路径先按峰值限制增益，'
        '写出 FLAC，再读回浮点，并在活动分析时不提供原混音参考。两条路径同时改变保存格式'
        '和活动分析输入，因此结果衡量整个路径，不能单独归因于量化精度。'
        'float 指下游直接读取浮点样本；SUG 与 MiliKara 的输入保留原生保存量化，并非无量化分离输出。',
        '下表缩写与[模型配置与选择](separation-survey.md)中的十种配置一一对应：',
        table(['缩写','模型配置'], [[name,label] for name,(label,_) in MODELS.items()]),
        DEFINITIONS,
        *[section for persist in ('float','pcm24') for mode in ('global','concat_core','concat_padded')
          for section in ('## ' + persist + '／' + labels[mode],
            metric_table([(name,next(r for r in rows if r['separator']==name and r['persistence']==persist and r['mode']==mode))
                          for name in MODELS]).replace('| 条件 |','| 模型 |',1))],
        '表中保留原始日语叶级单元（标注树中不再细分的最小定时对象）；'
        '跨删段的预测按无效处理。拉丁片段、潮汕话假名和逐曲结果另存。'
        '[完整指标](../results/separation-alignment/metrics.json)、'
        '[表格](../results/separation-alignment/tables.md)与'
        '[CSV](../results/separation-alignment/metrics.csv)可复核歌曲等权宏平均及原始计数。',
        '产品完整路线见[八路线比较](comparison.md)，独立资源测量见[分离资源](separation-performance.md)。'])

def resources():
    names = {'demucs': 'Demucs', 'bs': 'BS Karaoke', 'kim': 'Kim Vocals'}
    groups = {name: [read(f'ablation/resource-benchmark/{name}-{i}.json') for i in (1,2)] for name in names}
    rows = []
    for name,records in groups.items():
        assert len({r['weight_sha256'] for r in records}) == 1
        rows.append([names[name], *(f"{r['seconds']:.2f}" for r in records),
                     f"{statistics.mean(r['seconds'] for r in records):.2f}",
                     f"{statistics.mean(r['realtime_factor'] for r in records):.4f}",
                     f"{max(r['torch_peak_allocated_bytes'] for r in records)/2**30:.2f}",
                     max(r['nvidia_process_peak_mib_sampled'] for r in records),
                     f"{records[0]['weight_bytes']/2**20:.2f}"])
    write('resources.md', [
        '# 三条分离路径的资源测量',
        '在同一首 s01 上，每条路径以新进程运行两次，所有测量串行完成。'
        '权重已下载，GPU 环境与实际调用边界保存在逐次记录中。',
        '计时从入口导入和 CUDA 初始化之后开始，包含延迟导入、解码、模型加载、分离、'
        '原生输出检查与关闭；不包含下载、解释器启动与运行后的哈希计算。'
        '三个封装的附加检查和输出数量不同，因此比较的是实际入口成本。',
        table(['路径','第一次 s','第二次 s','平均 s','平均实时因子','Torch 峰值 GiB','采样进程显存 MiB','权重 MiB'],rows),
        '实时因子是处理耗时除以歌曲时长。Torch 峰值指张量分配，采样进程显存还包括框架上下文，'
        '两者不能互换；显存列取两次运行中的最大值。两次重复只用于检查本机运行稳定性。',
        '[六份原始记录](../results/ablation/resource-benchmark)保留环境、权重哈希与计时边界。'
        '十种配置预热后分离成本见[分离性能](separation-performance.md)，对齐质量见[八路线比较](comparison.md)。'])

def performance():
    rows=[]; identity=[]; memory=[]; export=[]
    for name,(label,_) in MODELS.items():
        both={device:read(f"separation-resources/{name}{'-cpu' if device=='cpu' else ''}.json") for device in ('cuda','cpu')}
        totals={}
        for device,data in both.items():
            assert len(data['records'])==(3 if device=='cpu' else 15)
            groups={s['id']:[r for r in data['records'] if r['song']==s['id']] for s in data['inputs']}
            assert all(len(rs)==3 for rs in groups.values())
            totals[device]=sum(statistics.median(r['seconds'] for r in rs) for rs in groups.values())
        gpu=both['cuda'];cpu=both['cpu']
        for device,data in both.items():
            export.append({'model':name,'device':device,'seconds':totals[device],'rss_bytes':max(r['rss_bytes'] for r in data['records']),
                'allocated_bytes':max((r['allocated_bytes'] for r in data['records'] if r['allocated_bytes'] is not None),default=None),
                'process_gpu_bytes':max((r.get('process_gpu_bytes') for r in data['records'] if r.get('process_gpu_bytes') is not None),default=None),
                'board_energy_joules':sum(statistics.median(r['board_energy_joules'] for r in data['records'] if r['song']==song['id']) for song in data['inputs']) if device=='cuda' else None,
                'input_scope':'rainbow-30-60' if device=='cpu' else 'five-full-songs',
                'runs':len(data['records'])})
        energy=sum(statistics.median(r['board_energy_joules'] for r in gpu['records'] if r['song']==song['id']) for song in gpu['inputs'])
        rows.append([label,f"{totals['cuda']:.2f}",f"{totals['cpu']:.2f}",f"{energy/1000:.2f}"])
        def peak(data,key):
            values=[r.get(key) for r in data['records'] if r.get(key) is not None]
            return f'{max(values)/2**30:.2f}' if values else '—'
        memory.append([label,peak(cpu,'rss_bytes'),peak(gpu,'rss_bytes'),peak(gpu,'allocated_bytes'),peak(gpu,'process_gpu_bytes') if name=='sug' else '—'])
        params=gpu['identity'].get('parameters')
        identity.append([label,f'{params/1e6:.3f}' if params is not None else '—',gpu['torch'],gpu['identity'].get('audio_separator','—')])
    with (ROOT/'results/separation-resources/summary.csv').open('w') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(export[0]));writer.writeheader();writer.writerows(export)
    (ROOT/'results/separation-resources/summary.json').write_text(json.dumps(export,ensure_ascii=False,indent=2)+'\n')
    write('separation-performance.md', [
        '# 十种人声分离配置的资源实测',
        'GPU 使用固定五首整曲，每首先以最多 30 秒预热，再重复三次；CPU 使用《Rainbow Flower》30–60 秒片段，预热一次后重复三次。十种配置共 180 次正式测量（GPU 150 次、CPU 30 次）。'
        'GPU 耗时与能量先逐曲取三次中位数，再对五曲求和；CPU 耗时取片段三次中位数，两种输入范围不用于计算设备加速比。内存与显存取全部运行的峰值。资源测量串行执行，与质量计算错开。',
        table(['配置','五曲 GPU s','30 秒片段 CPU s','GPU 板卡能量 kJ'],rows),
        '板卡能量按约 20 ms 间隔采样积分，包含空闲功耗。',
        table(['配置','CPU RSS GiB','GPU RSS GiB','Torch allocated GiB','ONNX 进程显存 GiB'],memory),
        'RSS（Resident Set Size，驻留集大小）统计进程树的物理内存驻留量，共享页可能重复计入。Torch allocated 为框架张量分配峰值；'
        'ONNX 进程显存包含运行时和设备上下文，两列分别呈现，不能直接排名。破折号表示不适用。',
        '## 固定条件与计时',
        '硬件为 NVIDIA GeForce RTX 4090（49140 MiB，驱动 595.58.03）与双路 AMD EPYC 7502。输入统一解码为 44.1 kHz 双声道；'
        '随机种子为 0，Torch 使用 8 线程，ONNX 使用 8 个计算线程与 1 个调度线程，有效 batch=1。保留各权重的分块、重叠和归一化；CPU 关闭 CUDA 混合精度并禁用 GPU。',
        '计时包含输入搬运、推理及结果返回 CPU，排除解码、模型加载、编码和写盘。文件入口通过内存适配调用相同算法，并与原生输出核验。'
        'BS Karaoke 的 CPU 路径沿用同一底层算法，仅适配设备与混合精度开关。',
        table(['配置','参数量／百万','Torch','audio-separator'],identity),
        'MDX-Net Inst HQ 3 按 ONNX 文件初始化张量的元素总量统计，包含归一化运行统计量；其他配置按 Torch 模型参数元素量统计。',
        '权重、配置、环境和逐次数据见[模型清单](../configs/separation-models.json)、[原始记录](../results/separation-resources)及'
        '[五曲输入](../configs/separation-resources-inputs.json)与 [CPU 片段](../configs/separation-cpu-inputs.json)。原生适配核验与人声来源见[下游数据目录](../results/separation-alignment)。'
        '单曲实际入口成本见[入口资源报告](resources.md)，固定下游端点见[分离与对齐](separation-alignment.md)。'])


def local():
    metrics = read('local-refinement/metrics.json')
    rows = {(r['baseline'], r['variant']): r for r in metrics
            if r['song'] == 'ALL' and r['group'] == 'japanese'}
    runtime = read('local-refinement/runtime.json')['records']
    names = {'global': '完整人声', 'concat_core': 'core 拼接'}
    variants = {'baseline': '保留首轮', 'cached_window': '复用概率', 'local_fresh': '局部声学重算'}
    n = rows['global', 'baseline']['n']
    songs = len({r['song'] for r in runtime})
    gains = [f"{names[b]}从 {rows[b, 'baseline']['hit100']} 增至 {rows[b, 'local_fresh']['hit100']}，"
             f"新增 {rows[b, 'local_fresh']['gained100']} 个命中、损失 {rows[b, 'local_fresh']['lost100']} 个"
             for b in names]
    write('local-refinement.md', [
        '# 人工读音下的异常行局部重算',
        f"固定 {songs} 首日语歌曲、{n} 个日语叶级单元（标注树中不再细分的最小定时对象）。"
        + '；'.join(gains) + '。',
        '## 方法与筛选',
        '所有条件使用人工读音、Demucs 人声、NextFire 与标准 CTC。' + CORE,
        '异常筛选包括跨删段、无有效时长、非末单元超过 2 秒或末单元超过 3 秒、'
        '活动覆盖低于 70%、平均单元置信度低于 0.60。每曲最多选取向上取整的 20% 行，'
        '所选音频总长不超过原音频的 20%，单窗不超过 35 秒。窗口取首轮行首尾各外扩 0.3 秒，'
        '对齐到 20 ms 网格；只运行一轮。筛选和接受规则不读取人工时间。'
        '[固定协议](../configs/local-refinement.json)与[决策记录](../results/local-refinement/decisions)保存完整规则及实际选择。',
        '局部声学重算重新计算原时间轴上连续人声窗口的概率；复用概率只裁剪首轮概率。'
        '两者共享筛选行和窗口，候选经过正时长、跨删段、活动覆盖、置信度和位移检查后才能采用。',
        '## 端点结果', DEFINITIONS,
        metric_table([(names[b] + '／' + variants[v], rows[b, v]) for b in names for v in variants]),
        '## 运行与适用范围',
        '本轮通过 CUDA 完成质量实验，任务可能与其他质量实验并行。'
        '逐曲耗时仅作为执行诊断，不能据此比较独占 GPU 时的运行速度。'
        '[计时记录](../results/local-refinement/runtime.json)保留首轮、复用概率和声学重算的实际耗时。',
        '这些结果评价固定异常筛选与接受规则。收益应同时结合命中、缺失与大误差判断，'
        '不能只按成功修复的个别行评价。当前 Lazulite Studio 产品输出另见[八路线比较](comparison.md)。'
        '[逐曲及拉丁单元指标](../results/local-refinement/metrics.json)与'
        '[原始预测](../results/local-refinement/predictions)可独立复核。'])

def milikara():
    metrics = read('milikara/metrics.json')
    rows = {r['experiment']: r for r in metrics if r['song'] == 'ALL' and r['group'] == 'japanese'}
    modes = {'global': '完整人声', 'concat_core': 'core 拼接', 'concat_padded': '带缓冲拼接'}
    configs = {'f00000': '标准 CTC', 'f00001': '仅自由尾部', 'f01111': '活动代价与自由尾部', 'f11111': '五项全开'}
    n = rows['global/f00000']['n']
    effects = [r for r in read('milikara/factor-effects.json') if r['song'] == 'ALL']
    write('milikara.md', [
        '# MiliKara 原生管线与解码机制',
        '原生完整管线已纳入[八路线三组比较](comparison.md)，统一比较人工读音、自带人声分离、'
        'BS Karaoke 人声与正文自动读音，采用全部路线的共同正文边界。'
        '下文保留解码模块的独立实验，不能把模块配置的成绩当作 MiliKara 默认产品成绩。',
        '## 解码模块与分母',
        f"本轮固定人工读音与 NextFire，使用 12 首日语歌曲的 {n} 个日语叶级单元"
        '（标注树中不再细分的最小定时对象）。拉丁单元和潮汕话假名转写单列。' + CORE,
        '模块实验读取冻结的人声活动边界和声学概率，使用经过等价核对的加速递推。'
        '五位配置码依次表示分隔符并入 blank（当前帧不输出文本标签的空白标签）、'
        '行内停顿代价、静音区停顿代价、静音区发音代价和自由尾部；0 为关闭，1 为开启。'
        '每种音频策略包含全部 32 种组合。',
        DEFINITIONS,
        metric_table([(modes[m] + '／' + label, rows[m + '/' + c]) for m in modes for c, label in configs.items()]),
        '## 开关配对效应',
        '对每个开关，在其他四项的 16 种组合上比较开与关的双端 100 ms 命中数差，再取均值。',
        table(['音频', '开关', '配对数', '平均命中数变化', '最小／最大变化'],
              [[modes[r['audio']], r['factor'], r['pairs'], f"{r['mean_hit100_delta']:+.2f}",
                f"{r['min_hit100_delta']:+d} / {r['max_hit100_delta']:+d}"] for r in effects]),
        '## 原混音与重试',
        '原混音由 FFmpeg 转为 16 kHz 单声道。重试实验保持目标文本和活动能量输入固定，'
        '保留上游窗口规划与音轨选择，原始输出记录实际重试路径。',
        metric_table([(modes[m] + '／' + label, rows[m + '/' + c]) for m in modes for c, label in
                      [('original-control-f00000', '原混音标准 CTC'),
                       ('audio-original-r1-d0', '原混音起步、允许重试'),
                       ('audio-vocals-r1-d0', '人声起步、允许原混音重试')]]),
        '## 复核',
        f"完整实验包括 {len(rows)} 个模块配置。窗口、人工行首、读音处理、能量尾点和声学上下文"
        '条件见[完整日语表](../results/milikara/tables-japanese.md)、'
        '[逐曲指标](../results/milikara/metrics.json)与[配对明细](../results/milikara/factor-effects.json)。'
        '人工行首条件属于诊断；全部失败仍保留评分分母。配置未按歌曲成绩选择。',
        '人工读音的异常行修复见[局部重算](local-refinement.md)；'
        '独立注音报告使用全部 12 首日语歌曲，另列 s11 日语部分，见[自动注音](auto-reading.md)。'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('reports', nargs='+', choices=['local', 'milikara', 'ablation', 'separation', 'timing', 'resources', 'performance'])
    args = parser.parse_args()
    for name in args.reports:
        globals()[name]()
