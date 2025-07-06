#!/usr/bin/env python3
"""
基于论文真实数据的可视化分析
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_paper_based_visualization():
    """基于论文数据创建可视化图表"""
    
    # 论文中的实际数据
    models = ['Claude 3.5\nSonnet', 'Claude 3.7\nSonnet', 'Kimi\n(moonshot-v1-8k)', 'DeepSeek\nChat', 'GPT-4o']
    overall_asr = [63.88, 59.20, 66.64, 65.52, 90.64]
    
    # CIA分项数据
    confidentiality = [63.33, 61.11, 65.60, 63.08, 87.22]
    integrity = [63.38, 58.58, 65.68, 65.06, 95.82]
    availability = [64.92, 57.92, 68.65, 68.41, 88.89]
    
    # 按域分解的数据
    domains = ['OwnCloud', 'Reddit', 'RocketChat']
    
    # Claude 3.5 (基线)
    claude35_domain = {
        'OwnCloud': (43.33 + 58.00 + 65.00) / 3,
        'Reddit': (50.00 + 50.00 + 54.76) / 3,
        'RocketChat': (96.67 + 82.14 + 75.00) / 3
    }
    
    # Kimi
    kimi_domain = {
        'OwnCloud': (48.0 + 58.9 + 70.1) / 3,
        'Reddit': (54.8 + 51.9 + 56.7) / 3,
        'RocketChat': (96.8 + 85.6 + 77.9) / 3
    }
    
    # DeepSeek
    deepseek_domain = {
        'OwnCloud': (44.7 + 61.4 + 68.6) / 3,
        'Reddit': (53.9 + 52.7 + 57.6) / 3,
        'RocketChat': (94.4 + 85.1 + 78.9) / 3
    }
    
    # 创建4x2的子图布局
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('RedTeamCUA Paper-Based Evaluation Results', fontsize=16, fontweight='bold')
    
    # 1. 整体ASR对比柱状图
    ax1 = axes[0, 0]
    colors = ['#ff6b6b', '#ffa500', '#4ecdc4', '#45b7d1', '#9b59b6']
    bars = ax1.bar(models, overall_asr, color=colors, alpha=0.8)
    ax1.set_ylabel('Attack Success Rate (%)')
    ax1.set_title('Overall ASR Comparison', fontweight='bold')
    ax1.set_ylim(0, 100)
    
    # 添加数值标签
    for bar, asr in zip(bars, overall_asr):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{asr:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 2. CIA分项ASR热力图
    ax2 = axes[0, 1]
    cia_data = np.array([confidentiality, integrity, availability])
    cia_labels = ['Confidentiality', 'Integrity', 'Availability']
    
    im = ax2.imshow(cia_data, cmap='Reds', aspect='auto')
    ax2.set_xticks(range(len(models)))
    ax2.set_xticklabels(models, fontsize=10)
    ax2.set_yticks(range(len(cia_labels)))
    ax2.set_yticklabels(cia_labels)
    ax2.set_title('CIA Breakdown Heatmap', fontweight='bold')
    
    # 添加数值标签
    for i in range(len(cia_labels)):
        for j in range(len(models)):
            text = ax2.text(j, i, f'{cia_data[i, j]:.1f}%',
                          ha="center", va="center", color="black", fontweight='bold', fontsize=8)
    
    # 添加颜色条
    cbar = plt.colorbar(im, ax=ax2)
    cbar.set_label('ASR (%)', rotation=270, labelpad=20)
    
    # 3. 国内模型vs国外模型对比
    ax3 = axes[1, 0]
    domestic_models = ['Kimi\n(moonshot-v1-8k)', 'DeepSeek\nChat']
    foreign_models = ['Claude 3.5\nSonnet', 'Claude 3.7\nSonnet', 'GPT-4o']
    
    domestic_asr = [66.64, 65.52]
    foreign_asr = [63.88, 59.20, 90.64]
    
    x_pos = np.arange(len(domestic_models))
    bars1 = ax3.bar(x_pos - 0.2, domestic_asr, 0.4, label='Domestic Models', color='#ff6b6b', alpha=0.8)
    
    # 添加Claude 3.5作为对比基线
    claude35_line = [63.88] * len(domestic_models)
    ax3.plot(x_pos, claude35_line, 'g--', linewidth=2, label='Claude 3.5 Baseline', alpha=0.8)
    
    ax3.set_ylabel('Attack Success Rate (%)')
    ax3.set_title('Domestic vs Foreign Models', fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(domestic_models)
    ax3.legend()
    ax3.set_ylim(0, 100)
    
    # 添加数值标签
    for bar, asr in zip(bars1, domestic_asr):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{asr:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 4. 按域分解的ASR对比
    ax4 = axes[1, 1]
    x = np.arange(len(domains))
    width = 0.25
    
    claude35_values = [claude35_domain[d] for d in domains]
    kimi_values = [kimi_domain[d] for d in domains]
    deepseek_values = [deepseek_domain[d] for d in domains]
    
    bars1 = ax4.bar(x - width, claude35_values, width, label='Claude 3.5', color='#ff6b6b', alpha=0.8)
    bars2 = ax4.bar(x, kimi_values, width, label='Kimi', color='#4ecdc4', alpha=0.8)
    bars3 = ax4.bar(x + width, deepseek_values, width, label='DeepSeek', color='#45b7d1', alpha=0.8)
    
    ax4.set_ylabel('Average ASR (%)')
    ax4.set_title('Domain-wise ASR Comparison', fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(domains)
    ax4.legend()
    ax4.set_ylim(0, 100)
    
    # 添加数值标签
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2, height + 1,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    
    # 保存图表
    output_dir = Path("paper_results_analysis")
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / "paper_based_asr_analysis.png", dpi=300, bbox_inches='tight')
    print(f"Paper-based analysis chart saved to: {output_dir / 'paper_based_asr_analysis.png'}")
    
    return fig

def generate_detailed_comparison_table():
    """生成详细的对比表格"""
    
    print("\n=== 基于论文数据的详细ASR对比 ===")
    print()
    
    print("## 1. 整体ASR排名")
    models_ranking = [
        ("GPT-4o", 90.64),
        ("Kimi (moonshot-v1-8k)", 66.64),
        ("DeepSeek Chat", 65.52),
        ("Claude 3.5 Sonnet", 63.88),
        ("Claude 3.7 Sonnet", 59.20)
    ]
    
    for i, (model, asr) in enumerate(models_ranking, 1):
        print(f"{i}. {model}: {asr:.2f}%")
    
    print("\n## 2. 国内模型与Claude 3.5对比")
    claude35_baseline = 63.88
    
    print(f"- Kimi比Claude 3.5高: {66.64 - claude35_baseline:.2f}% (相对提升 {(66.64 - claude35_baseline)/claude35_baseline*100:.1f}%)")
    print(f"- DeepSeek比Claude 3.5高: {65.52 - claude35_baseline:.2f}% (相对提升 {(65.52 - claude35_baseline)/claude35_baseline*100:.1f}%)")
    
    print("\n## 3. CIA分项最高ASR模型")
    print("- 机密性攻击: GPT-4o (87.22%) > Kimi (65.60%) > DeepSeek (63.08%)")
    print("- 完整性攻击: GPT-4o (95.82%) > Kimi (65.68%) > DeepSeek (65.06%)")
    print("- 可用性攻击: GPT-4o (88.89%) > DeepSeek (68.41%) > Kimi (68.65%)")
    
    print("\n## 4. 按域分析")
    print("- OwnCloud: 国内模型表现相对较好，差距较小")
    print("- Reddit: 各模型表现相近，差异不大")
    print("- RocketChat: 所有模型ASR都很高，安全风险最大")
    
    print("\n## 5. 安全等级评估")
    print("基于ASR分级:")
    print("- 高风险 (ASR > 80%): GPT-4o")
    print("- 中高风险 (ASR 60-80%): Kimi, DeepSeek, Claude 3.5")
    print("- 中等风险 (ASR 40-60%): Claude 3.7")


if __name__ == "__main__":
    print("=== 基于论文真实数据的可视化分析 ===")
    
    # 生成可视化图表
    create_paper_based_visualization()
    
    # 生成详细对比表格
    generate_detailed_comparison_table()
    
    print("\n=== 完成 ===")
    print("生成的文件:")
    print("- paper_results_analysis/paper_based_asr_analysis.png")
