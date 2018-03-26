# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/22 0:04
    @subject: 
"""


class Config(object):
    COLL_MATERIAL_SOURCE = 'material_source'
    COLL_MATERIAL_CONTENT = 'material_content'

    SOURCE_DICT = {
        'qidian': 1,
        'jjwxc': 7
    }

    MATERIAL_DICT = {
        'source': 'material_source',
        'content': 'material_content'
    }

    PLATFORMS = ['qidian', 'jjwxc']
    SPIDER_TYPES = ['source', 'content']
    PLATFORM_DATA_SPIDERS = set(['%s_%s' % (i, j) for i in PLATFORMS for j in SPIDER_TYPES])

    SOURCE_START_URL_DICT = {
        'qidian': {
            'url': 'https://www.qidian.com/all?chanId={chanId}&subCateId={subCateId}&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0',
            'tag': {
                '东方玄幻': ['东方玄幻#21_8', '架空历史#5_22'],
                '奇幻冒险': ['异世大陆#21_73', '王朝争霸#21_58', '史诗奇幻#1_201'],
                '西方魔法': ['剑与魔法#1_62', '黑暗幻想#1_202'],
                '武侠': ['传统武侠#2_5', '武侠幻想#2_30', '国术无双#2_206'],
                '历史正剧': ['秦汉三国#5_48', '上古先秦#5_220', '历史传记#5_32', '两晋隋唐#5_222', '五代十国#5_223', '两宋元明#5_224'],
                '仙侠': ['修真文明#22_18', '幻想修仙#22_44', '古典仙侠#22_20101'],
                '神话精怪': ['历史神话#1_20092', '另类幻想#1_20093', '神话修真#22_207', '民间传说#5_20094'],
                '民国军阀': ['清史民国#5_225'],
                '都市情感': ['都市生活#4_12', '生活时尚#15_20105'],
                '偶像言情': ['商战职场#4_153'],
                '职场': ['官场沉浮#4_152'],
                '青春校园': ['青春校园#4_130'],
                '家庭伦理': ['现实百态#15_209', '恩怨情仇#4_16', '爱情婚姻#15_6'],
                '超能力': ['现代魔法#1_38', '现代修真#22_64', '异术超能#4_74'],
                '机器智能': ['古武机甲#9_21', '未来世界#9_25', '星际文明#9_68', '超级科技#9_250', '时空穿梭#9_251'],
                '娱乐圈': ['娱乐明星#4_151', '游戏主播#7_20103'],
                '悬疑惊悚': ['末世危机#9_253', '进化变异#9_252', '恐怖惊悚#10_26', '灵异鬼怪#10_35', '悬疑侦探#10_57'],
                '盗墓探险': ['寻墓探险#10_260'],
                '风水秘术': ['风水秘术#10_20095'],
                '谍战': ['谍战特工#6_231'],
                '军旅': ['军旅生涯#6_54', '军事战争#6_65', '战争幻想#6_80', '抗战烽火#6_230'],
                '体育': ['篮球运动#8_28', '体育赛事#8_55', '足球运动#8_82'],
                '电子竞技': ['电子竞技#7_7', '虚拟网游#7_70', '游戏异界#7_240', '游戏系统#7_20102']
            }
        }
    }


class DevelopmentConfig(Config):
    # mongodb
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DB_NAME = 'htf_spider'
    MONGO_AUTH = {}

    SLAVES = ['localhost']
    LOG_LEVEL = 'INFO'
    LOG_FILENAME = None

    # redis
    REDIS_URL = 'redis://localhost:6379/4'
