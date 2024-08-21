from django.http import JsonResponse
from django.db.models import Avg, Count
from .models import GraphModel
import numpy as np
from decimal import Decimal
from datetime import datetime, timedelta

def generate_graphs_data(request):
    data = GraphModel.objects.all()

    # Bar chart data
    bar_data = {
        'labels': ['CHW_IN_TEMP', 'CHW_OUT_TEMP', 'COW_IN_TEMP', 'COW_OUT_TEMP', 'STEAM_COND_TEMP', 'HTG_TEMP', 'LTG_TEMP', 'HTHE_OUT_TEMP', 'SPRAY_TEMP', 'DL_SLN_TEMP', 'REF_TEMP', 'U_TUBE_TEMP', 'OVRFLW_LTG_TEMP', 'HTG_TOP_TEMP', 'HTG_BOT_TEMP', 'HTG_TB_ABS_DIFF_TEMP', 'VACCUM_PR', 'REF_TEMP_LOW_SP', 'REF_TEMP_LOW_HYS', 'HTG_PR_HI_SP', 'HTG_PR_LOW_LMT_SP', 'HTG_PR_HI_LMT_SP', 'HTG_PR_HI_HYS', 'HTG_VAP_TEMP', 'TIME'],
        'datasets': [{
            'label': 'Average Temperatures',
            'data': [
                data.aggregate(Avg('chw_in_temp'))['chw_in_temp__avg'],
                data.aggregate(Avg('chw_out_temp'))['chw_out_temp__avg'],
                data.aggregate(Avg('cow_in_temp'))['cow_in_temp__avg'],
                data.aggregate(Avg('cow_out_temp'))['cow_out_temp__avg'],
                data.aggregate(Avg('steam_cond_temp'))['steam_cond_temp__avg'],
                data.aggregate(Avg('htg_temp'))['htg_temp__avg'],
                data.aggregate(Avg('ltg_temp'))['ltg_temp__avg'],
                data.aggregate(Avg('hthe_out_temp'))['hthe_out_temp__avg'],
                data.aggregate(Avg('spray_temp'))['spray_temp__avg'],
                data.aggregate(Avg('dl_sln_temp'))['dl_sln_temp__avg'],
                data.aggregate(Avg('ref_temp'))['ref_temp__avg'],
                data.aggregate(Avg('u_tube_temp'))['u_tube_temp__avg'],
                data.aggregate(Avg('ovrflw_ltg_temp'))['ovrflw_ltg_temp__avg'],
                data.aggregate(Avg('htg_top_temp'))['htg_top_temp__avg'],
                data.aggregate(Avg('htg_bot_temp'))['htg_bot_temp__avg'],
                data.aggregate(Avg('htg_tb_abs_diff_temp'))['htg_tb_abs_diff_temp__avg'],
                data.aggregate(Avg('vaccum_pr'))['vaccum_pr__avg'],
                data.aggregate(Avg('ref_temp_low_sp'))['ref_temp_low_sp__avg'],
                data.aggregate(Avg('ref_temp_low_hys'))['ref_temp_low_hys__avg'],
                data.aggregate(Avg('htg_pr_hi_sp'))['htg_pr_hi_sp__avg'],
                data.aggregate(Avg('htg_pr_low_lmt_sp'))['htg_pr_low_lmt_sp__avg'],
                data.aggregate(Avg('htg_pr_hi_lmt_sp'))['htg_pr_hi_lmt_sp__avg'],
                data.aggregate(Avg('htg_pr_hi_hys'))['htg_pr_hi_hys__avg'],
                data.aggregate(Avg('htg_vap_temp'))['htg_vap_temp__avg'],
                data.aggregate(Avg('time'))['time__avg']
            ],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)',
                'rgba(102, 255, 178, 0.6)',
                'rgba(255, 102, 178, 0.6)',
                'rgba(178, 102, 255, 0.6)',
                'rgba(102, 178, 255, 0.6)',
                'rgba(255, 178, 102, 0.6)',
                'rgba(178, 255, 102, 0.6)',
                'rgba(102, 255, 102, 0.6)',
                'rgba(255, 102, 102, 0.6)',
                'rgba(102, 102, 255, 0.6)',
                'rgba(255, 255, 102, 0.6)',
                'rgba(102, 255, 255, 0.6)',
                'rgba(255, 102, 255, 0.6)',
                'rgba(178, 178, 178, 0.6)',
                'rgba(255, 178, 178, 0.6)',
                'rgba(178, 255, 178, 0.6)',
                'rgba(178, 178, 255, 0.6)',
                'rgba(255, 255, 178, 0.6)',
                'rgba(178, 255, 255, 0.6)',
                'rgba(255, 178, 255, 0.6)'
            ],
        }]
    }

    # Line chart data
    line_data = {
        'labels': list(data.values_list('id', flat=True)),
        'datasets': [
            {'label': 'CHW_IN_TEMP', 'data': list(data.values_list('chw_in_temp', flat=True)), 'borderColor': 'rgb(255, 99, 132)'},
            {'label': 'CHW_OUT_TEMP', 'data': list(data.values_list('chw_out_temp', flat=True)), 'borderColor': 'rgb(54, 162, 235)'},
            {'label': 'COW_IN_TEMP', 'data': list(data.values_list('cow_in_temp', flat=True)), 'borderColor': 'rgb(255, 206, 86)'},
            {'label': 'COW_OUT_TEMP', 'data': list(data.values_list('cow_out_temp', flat=True)), 'borderColor': 'rgb(75, 192, 192)'},
            {'label': 'STEAM_COND_TEMP', 'data': list(data.values_list('steam_cond_temp', flat=True)), 'borderColor': 'rgb(153, 102, 255)'},
            {'label': 'HTG_TEMP', 'data': list(data.values_list('htg_temp', flat=True)), 'borderColor': 'rgb(255, 159, 64)'},
            {'label': 'LTG_TEMP', 'data': list(data.values_list('ltg_temp', flat=True)), 'borderColor': 'rgb(102, 255, 178)'},
            {'label': 'HTHE_OUT_TEMP', 'data': list(data.values_list('hthe_out_temp', flat=True)), 'borderColor': 'rgb(255, 102, 178)'},
            {'label': 'SPRAY_TEMP', 'data': list(data.values_list('spray_temp', flat=True)), 'borderColor': 'rgb(178, 102, 255)'},
            {'label': 'DL_SLN_TEMP', 'data': list(data.values_list('dl_sln_temp', flat=True)), 'borderColor': 'rgb(102, 178, 255)'},
            {'label': 'REF_TEMP', 'data': list(data.values_list('ref_temp', flat=True)), 'borderColor': 'rgb(255, 178, 102)'},
            {'label': 'U_TUBE_TEMP', 'data': list(data.values_list('u_tube_temp', flat=True)), 'borderColor': 'rgb(178, 255, 102)'},
            {'label': 'OVRFLW_LTG_TEMP', 'data': list(data.values_list('ovrflw_ltg_temp', flat=True)), 'borderColor': 'rgb(102, 255, 102)'},
            {'label': 'HTG_TOP_TEMP', 'data': list(data.values_list('htg_top_temp', flat=True)), 'borderColor': 'rgb(255, 102, 102)'},
            {'label': 'HTG_BOT_TEMP', 'data': list(data.values_list('htg_bot_temp', flat=True)), 'borderColor': 'rgb(102, 102, 255)'},
            {'label': 'HTG_TB_ABS_DIFF_TEMP', 'data': list(data.values_list('htg_tb_abs_diff_temp', flat=True)), 'borderColor': 'rgb(255, 255, 102)'},
            {'label': 'VACCUM_PR', 'data': list(data.values_list('vaccum_pr', flat=True)), 'borderColor': 'rgb(102, 255, 255)'},
            {'label': 'REF_TEMP_LOW_SP', 'data': list(data.values_list('ref_temp_low_sp', flat=True)), 'borderColor': 'rgb(255, 102, 255)'},
            {'label': 'REF_TEMP_LOW_HYS', 'data': list(data.values_list('ref_temp_low_hys', flat=True)), 'borderColor': 'rgb(178, 178, 178)'},
            {'label': 'HTG_PR_HI_SP', 'data': list(data.values_list('htg_pr_hi_sp', flat=True)), 'borderColor': 'rgb(255, 178, 178)'},
            {'label': 'HTG_PR_LOW_LMT_SP', 'data': list(data.values_list('htg_pr_low_lmt_sp', flat=True)), 'borderColor': 'rgb(178, 255, 178)'},
            {'label': 'HTG_PR_HI_LMT_SP', 'data': list(data.values_list('htg_pr_hi_lmt_sp', flat=True)), 'borderColor': 'rgb(178, 178, 255)'},
            {'label': 'HTG_PR_HI_HYS', 'data': list(data.values_list('htg_pr_hi_hys', flat=True)), 'borderColor': 'rgb(255, 255, 178)'},
            {'label': 'HTG_VAP_TEMP', 'data': list(data.values_list('htg_vap_temp', flat=True)), 'borderColor': 'rgb(178, 255, 255)'},
            {'label': 'TIME', 'data': list(data.values_list('time', flat=True)), 'borderColor': 'rgb(255, 178, 255)'}
        ]
    }

    # Pie chart data
    temp_ranges = {
        'Low': data.filter(chw_in_temp__lt=20).count(),
        'Medium': data.filter(chw_in_temp__gte=20, chw_in_temp__lt=30).count(),
        'High': data.filter(chw_in_temp__gte=30).count()
    }
    pie_data = {
        'labels': list(temp_ranges.keys()),
        'datasets': [{
            'data': list(temp_ranges.values()),
            'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56'],
        }]
    }

    # Scatter plot data
    scatter_data = {
        'datasets': [{
            'label': 'CHW_IN_TEMP vs COW_OUT_TEMP',
            'data': [{'x': x, 'y': y} for x, y in zip(data.values_list('chw_in_temp', flat=True), data.values_list('cow_out_temp', flat=True))],
            'backgroundColor': 'rgba(75, 192, 192, 0.6)'
        }]
    }

    # Heatmap data
    heatmap_data = {
    'z': [
        list(data.values_list('chw_in_temp', flat=True)),
        list(data.values_list('chw_out_temp', flat=True)),
        list(data.values_list('cow_in_temp', flat=True)),
        list(data.values_list('cow_out_temp', flat=True)),
        list(data.values_list('steam_cond_temp', flat=True)),
        list(data.values_list('htg_temp', flat=True)),
        list(data.values_list('ltg_temp', flat=True)),
        list(data.values_list('hthe_out_temp', flat=True)),
        list(data.values_list('spray_temp', flat=True)),
        list(data.values_list('dl_sln_temp', flat=True)),
        list(data.values_list('ref_temp', flat=True)),
        list(data.values_list('u_tube_temp', flat=True)),
        list(data.values_list('ovrflw_ltg_temp', flat=True)),
        list(data.values_list('htg_top_temp', flat=True)),
        list(data.values_list('htg_bot_temp', flat=True)),
        list(data.values_list('htg_tb_abs_diff_temp', flat=True)),
        list(data.values_list('vaccum_pr', flat=True)),
        list(data.values_list('ref_temp_low_sp', flat=True)),
        list(data.values_list('ref_temp_low_hys', flat=True)),
        list(data.values_list('htg_pr_hi_sp', flat=True)),
        list(data.values_list('htg_pr_low_lmt_sp', flat=True)),
        list(data.values_list('htg_pr_hi_lmt_sp', flat=True)),
        list(data.values_list('htg_pr_hi_hys', flat=True)),
        list(data.values_list('htg_vap_temp', flat=True)),
        list(data.values_list('time', flat=True))
    ],
    'x': list(range(len(data))),
    'y': ['CHW_IN_TEMP', 'CHW_OUT_TEMP', 'COW_IN_TEMP', 'COW_OUT_TEMP', 'STEAM_COND_TEMP', 'HTG_TEMP', 'LTG_TEMP', 'HTHE_OUT_TEMP', 'SPRAY_TEMP', 'DL_SLN_TEMP', 'REF_TEMP', 'U_TUBE_TEMP', 'OVRFLW_LTG_TEMP', 'HTG_TOP_TEMP', 'HTG_BOT_TEMP', 'HTG_TB_ABS_DIFF_TEMP', 'VACCUM_PR', 'REF_TEMP_LOW_SP', 'REF_TEMP_LOW_HYS', 'HTG_PR_HI_SP', 'HTG_PR_LOW_LMT_SP', 'HTG_PR_HI_LMT_SP', 'HTG_PR_HI_HYS', 'HTG_VAP_TEMP', 'TIME']
}

    # Histogram data
    histogram_data = {
    'CHW_IN_TEMP': list(data.values_list('chw_in_temp', flat=True)),
    'CHW_OUT_TEMP': list(data.values_list('chw_out_temp', flat=True)),
    'COW_IN_TEMP': list(data.values_list('cow_in_temp', flat=True)),
    'COW_OUT_TEMP': list(data.values_list('cow_out_temp', flat=True)),
    'STEAM_COND_TEMP': list(data.values_list('steam_cond_temp', flat=True)),
    'HTG_TEMP': list(data.values_list('htg_temp', flat=True)),
    'LTG_TEMP': list(data.values_list('ltg_temp', flat=True)),
    'HTHE_OUT_TEMP': list(data.values_list('hthe_out_temp', flat=True)),
    'SPRAY_TEMP': list(data.values_list('spray_temp', flat=True)),
    'DL_SLN_TEMP': list(data.values_list('dl_sln_temp', flat=True)),
    'REF_TEMP': list(data.values_list('ref_temp', flat=True)),
    'U_TUBE_TEMP': list(data.values_list('u_tube_temp', flat=True)),
    'OVRFLW_LTG_TEMP': list(data.values_list('ovrflw_ltg_temp', flat=True)),
    'HTG_TOP_TEMP': list(data.values_list('htg_top_temp', flat=True)),
    'HTG_BOT_TEMP': list(data.values_list('htg_bot_temp', flat=True)),
    'HTG_TB_ABS_DIFF_TEMP': list(data.values_list('htg_tb_abs_diff_temp', flat=True)),
    'VACCUM_PR': list(data.values_list('vaccum_pr', flat=True)),
    'REF_TEMP_LOW_SP': list(data.values_list('ref_temp_low_sp', flat=True)),
    'REF_TEMP_LOW_HYS': list(data.values_list('ref_temp_low_hys', flat=True)),
    'HTG_PR_HI_SP': list(data.values_list('htg_pr_hi_sp', flat=True)),
    'HTG_PR_LOW_LMT_SP': list(data.values_list('htg_pr_low_lmt_sp', flat=True)),
    'HTG_PR_HI_LMT_SP': list(data.values_list('htg_pr_hi_lmt_sp', flat=True)),
    'HTG_PR_HI_HYS': list(data.values_list('htg_pr_hi_hys', flat=True)),
    'HTG_VAP_TEMP': list(data.values_list('htg_vap_temp', flat=True)),
    'TIME': list(data.values_list('time', flat=True))
}

    # Box plot data
    box_plot_data = [
    {'y': list(data.values_list('chw_in_temp', flat=True)), 'name': 'CHW_IN_TEMP'},
    {'y': list(data.values_list('chw_out_temp', flat=True)), 'name': 'CHW_OUT_TEMP'},
    {'y': list(data.values_list('cow_in_temp', flat=True)), 'name': 'COW_IN_TEMP'},
    {'y': list(data.values_list('cow_out_temp', flat=True)), 'name': 'COW_OUT_TEMP'},
    {'y': list(data.values_list('steam_cond_temp', flat=True)), 'name': 'STEAM_COND_TEMP'},
    {'y': list(data.values_list('htg_temp', flat=True)), 'name': 'HTG_TEMP'},
    {'y': list(data.values_list('ltg_temp', flat=True)), 'name': 'LTG_TEMP'},
    {'y': list(data.values_list('hthe_out_temp', flat=True)), 'name': 'HTHE_OUT_TEMP'},
    {'y': list(data.values_list('spray_temp', flat=True)), 'name': 'SPRAY_TEMP'},
    {'y': list(data.values_list('dl_sln_temp', flat=True)), 'name': 'DL_SLN_TEMP'},
    {'y': list(data.values_list('ref_temp', flat=True)), 'name': 'REF_TEMP'},
    {'y': list(data.values_list('u_tube_temp', flat=True)), 'name': 'U_TUBE_TEMP'},
    {'y': list(data.values_list('ovrflw_ltg_temp', flat=True)), 'name': 'OVRFLW_LTG_TEMP'},
    {'y': list(data.values_list('htg_top_temp', flat=True)), 'name': 'HTG_TOP_TEMP'},
    {'y': list(data.values_list('htg_bot_temp', flat=True)), 'name': 'HTG_BOT_TEMP'},
    {'y': list(data.values_list('htg_tb_abs_diff_temp', flat=True)), 'name': 'HTG_TB_ABS_DIFF_TEMP'},
    {'y': list(data.values_list('vaccum_pr', flat=True)), 'name': 'VACCUM_PR'},
    {'y': list(data.values_list('ref_temp_low_sp', flat=True)), 'name': 'REF_TEMP_LOW_SP'},
    {'y': list(data.values_list('ref_temp_low_hys', flat=True)), 'name': 'REF_TEMP_LOW_HYS'},
    {'y': list(data.values_list('htg_pr_hi_sp', flat=True)), 'name': 'HTG_PR_HI_SP'},
    {'y': list(data.values_list('htg_pr_low_lmt_sp', flat=True)), 'name': 'HTG_PR_LOW_LMT_SP'},
    {'y': list(data.values_list('htg_pr_hi_lmt_sp', flat=True)), 'name': 'HTG_PR_HI_LMT_SP'},
    {'y': list(data.values_list('htg_pr_hi_hys', flat=True)), 'name': 'HTG_PR_HI_HYS'},
    {'y': list(data.values_list('htg_vap_temp', flat=True)), 'name': 'HTG_VAP_TEMP'},
    {'y': list(data.values_list('time', flat=True)), 'name': 'TIME'}
]

    return JsonResponse({
    'bar_chart': bar_data,
    'line_chart': line_data,
    'pie_chart': pie_data,
    'scatter_chart': scatter_data,
    'heatmap_data': heatmap_data,
    'histogram_data': histogram_data,
    'box_plot_data': box_plot_data,
})