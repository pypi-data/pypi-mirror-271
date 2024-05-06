
####################################################################################################
#                                         算法一览
####################################################################################################
algorithm_glance = {
    # 10000
    "image": [
    ],
    
    "qrcode": [
        {
            "algorithm_id": "20001",
            "cn_name": "添加底色",
            "en_name": "under_color",
            "description": "给二维码添加纯色底色，可以设置底色颜色、横向扩展宽度和纵向扩展宽度，以及圆角大小。"
        },
    ],
    
    "logo": [
        # {
        #     "algorithm_id": 30001,
        #     "cn_name": "拆分选择",
        #     "en_name": "split_select",
        #     "description": "对logo进行图文拆分，然后选择其中一个拆分后的小图。"
        # },
        # {
        #     "algorithm_id": 30002,
        #     "cn_name": "拆分重构",
        #     "en_name": "split_restruct",
        #     "description": "对logo进行图文拆分，然后选择其中两个拆分后的小图进行重构。"
        # },
        {
            "algorithm_id": "30003",
            "cn_name": "描边",
            "en_name": "outline",
            "description": "给logo外轮廓描纯色边"
        },
        {
            "algorithm_id": "30004",
            "cn_name": "反色",
            "en_name": "binary",
            "description": "对logo进行反色处理，可指定前景颜色。"
        },
        {
            "algorithm_id": "30005",
            "cn_name": "直接平铺",
            "en_name": "direct_tile",
            "description": "单元素网格对齐平铺。"
        },
        {
            "algorithm_id": "30006",
            "cn_name": "交错平铺",
            "en_name": "intersect_tile",
            "description": "单元素行间交错平铺。"
        },
        {
            "algorithm_id": "30007",
            "cn_name": "随机平铺",
            "en_name": "random_tile",
            "description": "单元素随机位置平铺。"
        },
        {
            "algorithm_id": "30008",
            "cn_name": "虚实平铺",
            "en_name": "hollow_solid_tile",
            "description": "空心logo背景双实心logo平铺。"
        },
        {
            "algorithm_id": "30009",
            "cn_name": "旋转图像",
            "en_name": "rotate_image",
            "description": "固定图像中心旋转图像。"
        },
        {
            "algorithm_id": "30010",
            "cn_name": "翻转图像",
            "en_name": "flip_image",
            "description": "左右翻转 上下翻转 上下左右翻转 对阵转置"
        },
        {
            "algorithm_id": "30011",
            "cn_name": "深浅着色",
            "en_name": "depth_double_color",
            "description": "深浅背景前景的效果"
        },
    ],
    
    # 40000
    "text": [
    ],
    
    # 50000
    "svgPath": [
    ],
    
    # 60000
    "infoGroup": [
    ],
}




####################################################################################################
#                                         各个算法开放的参数
####################################################################################################
algorithm_parameters = {
    "20001": {
        "algorithm_id": "20001",
        "cn_name": "添加底色",
        "en_name": "under_color",
        "description": "给二维码添加纯色底色，可以设置底色颜色、横向扩展宽度和纵向扩展宽度，以及圆角大小。",
        "version": "v1",
        "version_list": {
            "v1": [
                {
                    "param_cn_name": "颜色",
                    "param_en_name": "color",
                    "param_description": "二维码底下的颜色",
                    "param_input_type": "multiBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [
                        {
                            "cn": "手动设定颜色",
                            "en": "manual",
                            "children":{
                                "data_type": "str",
                                "data_verify": r"^#[0-9A-Fa-f]{6,6}$",
                                "limit_low": 0,
                                "limit_high": 100,
                                # "length_min": 0,
                                # "length_max": 100,
                                "value": "#FFFFFF",
                            }
                        },
                        {
                            "cn": "跟随预定颜色",
                            "en": "follow",
                        },
                    ],
                    "option": "follow",
                    "header_list": [],
                    "array_list": [],
                },
                # {
                #     "param_cn_name": "横向扩展宽度",
                #     "param_en_name": "expand_horizontal",
                #     "param_description": "对二维码添加底色时，水平方向向外扩展的像素宽度",
                #     "param_input_type": "textBox",
                #     "data_type": "float",
                #     "data_verify": "",
                #     "limit_low": 0,
                #     "limit_high": 100,
                #     # "length_min": 0,
                #     # "length_max": 100,
                #     "value": 20,
                #     "option_list": [],
                #     "option": "",
                #     "header_list": [],
                #     "array_list": [],
                # },
                # {
                #     "param_cn_name": "纵向扩展宽度",
                #     "param_en_name": "expand_vertical",
                #     "param_description": "对二维码添加底色时，垂直方向向外扩展的像素宽度",
                #     "param_input_type": "textBox",
                #     "data_type": "float",
                #     "data_verify": "",
                #     "limit_low": 0,
                #     "limit_high": 100,
                #     # "length_min": 0,
                #     # "length_max": 100,
                #     "value": 20,
                #     "option_list": [],
                #     "option": "",
                #     "header_list": [],
                #     "array_list": [],
                # },
                # {
                #     "param_cn_name": "圆角大小",
                #     "param_en_name": "corner_radius",
                #     "param_description": "对二维码添加底色时，四个圆角的半径",
                #     "param_input_type": "textBox",
                #     "data_type": "float",
                #     "data_verify": "",
                #     "limit_low": 0,
                #     "limit_high": 100,
                #     # "length_min": 0,
                #     # "length_max": 100,
                #     "value": 20,
                #     "option_list": [],
                #     "option": "",
                #     "header_list": [],
                #     "array_list": [],
                # },
            ],
        }
    },
    
    # 30001: {
    #     "algorithm_id": 30001,
    #     "cn_name": "拆分选择",
    #     "en_name": "split_select",
    #     "description": "对logo进行图文拆分，然后选择其中一个拆分后的小图。",
    #     "version": "v1",
    #     "version_list": {
    #         "v1": [
    #             {
    #                 "param_cn_name": "选择项",
    #                 "param_en_name": "select",
    #                 "param_description": "选择一个拆分后的小图",
    #                 "param_input_type": "selectBox",
    #                 "data_type": "",
    #                 "data_verify": "",
    #                 "limit_low": 0,
    #                 "limit_high": 100,
    #                 # "length_min": 0,
    #                 # "length_max": 100,
    #                 "value": 0,
    #                 "option_list": [
    #                     {
    #                         "cn": "图",
    #                         "en": "graph",
    #                     },
    #                     {
    #                         "cn": "主文",
    #                         "en": "body_text",
    #                     },
    #                     {
    #                         "cn": "文字组",
    #                         "en": "text",
    #                     },
    #                     {
    #                         "cn": "icon",
    #                         "en": "icon",
    #                     },
    #                 ],
    #                 "option": "graph",
    #                 "header_list": [],
    #                 "array_list": [],
    #             },
    #         ]
    #     }
    # },
    
    # 30002: {
    #     "algorithm_id": 30002,
    #     "cn_name": "拆分重构",
    #     "en_name": "split_restruct",
    #     "description": "对logo进行图文拆分，然后选择其中两个拆分后的小图进行重构。",
    #     "version": "v1",
    #     "version_list": {
    #         "v1": [
    #             {
    #                 "param_cn_name": "选择项1",
    #                 "param_en_name": "select1",
    #                 "param_description": "选择第一个拆分后的小图",
    #                 "param_input_type": "selectBox",
    #                 "data_type": "",
    #                 "data_verify": "",
    #                 "limit_low": 0,
    #                 "limit_high": 100,
    #                 # "length_min": 0,
    #                 # "length_max": 100,
    #                 "value": 0,
    #                 "option_list": [
    #                     {
    #                         "cn": "图",
    #                         "en": "graph",
    #                     },
    #                     {
    #                         "cn": "主文",
    #                         "en": "body_text",
    #                     },
    #                     {
    #                         "cn": "文字组",
    #                         "en": "text",
    #                     },
    #                 ],
    #                 "option": "graph",
    #                 "header_list": [],
    #                 "array_list": [],
    #             },
    #             {
    #                 "param_cn_name": "选择项2",
    #                 "param_en_name": "select2",
    #                 "param_description": "选择第二个拆分后的小图",
    #                 "param_input_type": "selectBox",
    #                 "data_type": "",
    #                 "data_verify": "",
    #                 "limit_low": 0,
    #                 "limit_high": 100,
    #                 # "length_min": 0,
    #                 # "length_max": 100,
    #                 "value": 0,
    #                 "option_list": [
    #                     {
    #                         "cn": "图",
    #                         "en": "graph",
    #                     },
    #                     {
    #                         "cn": "主文",
    #                         "en": "body_text",
    #                     },
    #                     {
    #                         "cn": "文字组",
    #                         "en": "text",
    #                     },
    #                 ],
    #                 "option": "body_text",
    #                 "header_list": [],
    #                 "array_list": [],
    #             },
    #             {
    #                 "param_cn_name": "重构方式",
    #                 "param_en_name": "pattern",
    #                 "param_description": "重构方式",
    #                 "param_input_type": "selectBox",
    #                 "data_type": "",
    #                 "data_verify": "",
    #                 "limit_low": 0,
    #                 "limit_high": 100,
    #                 # "length_min": 0,
    #                 # "length_max": 100,
    #                 "value": 0,
    #                 "option_list": [
    #                     {
    #                         "cn": "上下",
    #                         "en": "top_bottom",
    #                     },
    #                     {
    #                         "cn": "下上",
    #                         "en": "bottom_top",
    #                     },
    #                     {
    #                         "cn": "左右",
    #                         "en": "left_right",
    #                     },
    #                     {
    #                         "cn": "左右",
    #                         "en": "right_left",
    #                     },
    #                 ],
    #                 "option": "top_bottom",
    #                 "header_list": [],
    #                 "array_list": [],
    #             },
    #             {
    #                 "param_cn_name": "四边对齐",
    #                 "param_en_name": "if_align",
    #                 "param_description": "是否对齐四边",
    #                 "param_input_type": "selectBox",
    #                 "data_type": "",
    #                 "data_verify": "",
    #                 "limit_low": 0,
    #                 "limit_high": 100,
    #                 # "length_min": 0,
    #                 # "length_max": 100,
    #                 "value": 0,
    #                 "option_list": [
    #                     {
    #                         "cn": "是",
    #                         "en": "yes",
    #                     },
    #                     {
    #                         "cn": "否",
    #                         "en": "not",
    #                     },
    #                 ],
    #                 "option": "yes",
    #                 "header_list": [],
    #                 "array_list": [],
    #             },
    #         ]
    #     }
    # },
    
    "30003": {
        "algorithm_id": "30003",
        "cn_name": "描边",
        "en_name": "outline",
        "description": "给logo外轮廓描纯色边",
        "version": "v2",
        "version_list": {
            "v1": [
                {
                    "param_cn_name": "描边宽度",
                    "param_en_name": "thickness",
                    "param_description": "描边的像素宽度",
                    "param_input_type": "textBox",
                    "data_type": "float",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 30,
                    "option_list": [],
                    "option": "",
                    "header_list": [],
                    "array_list": [],
                },
                {
                    "param_cn_name": "颜色",
                    "param_en_name": "color",
                    "param_description": "描边的颜色",
                    "param_input_type": "multiBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [
                        {
                            "cn": "手动设定颜色",
                            "en": "manual",
                            "children":{
                                "data_type": "str",
                                "data_verify": r"^#[0-9A-Fa-f]{6,6}$",
                                "limit_low": 0,
                                "limit_high": 100,
                                # "length_min": 0,
                                # "length_max": 100,
                                "value": "#FFFFFF",
                            }
                        },
                        {
                            "cn": "跟随预定颜色",
                            "en": "follow",
                        },
                    ],
                    "option": "follow",
                    "header_list": [],
                    "array_list": [],
                },
                {
                    "param_cn_name": "内填充",
                    "param_en_name": "if_fill",
                    "param_description": "是否填充内部空洞",
                    "param_input_type": "selectBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [
                        {
                            "cn": "是",
                            "en": "yes",
                        },
                        {
                            "cn": "否",
                            "en": "not",
                        },
                    ],
                    "option": "yes",
                    "header_list": [],
                    "array_list": [],
                }
            ],
            "v2": [
                {
                    "param_cn_name": "描边宽度",
                    "param_en_name": "thickness",
                    "param_description": "描边的像素宽度",
                    "param_input_type": "textBox",
                    "data_type": "float",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 30,
                    "option_list": [],
                    "option": "",
                    "header_list": [],
                    "array_list": [],
                },
                {
                    "param_cn_name": "颜色",
                    "param_en_name": "color",
                    "param_description": "描边的颜色",
                    "param_input_type": "multiBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [
                        {
                            "cn": "手动设定颜色",
                            "en": "manual",
                            "children":{
                                "data_type": "str",
                                "data_verify": r"^#[0-9A-Fa-f]{6,6}$",
                                "limit_low": 0,
                                "limit_high": 100,
                                # "length_min": 0,
                                # "length_max": 100,
                                "value": "#FFFFFF",
                            }
                        },
                        {
                            "cn": "跟随预定颜色",
                            "en": "follow",
                        },
                    ],
                    "option": "follow",
                    "header_list": [],
                    "array_list": [],
                },
                {
                    "param_cn_name": "内填充",
                    "param_en_name": "if_fill",
                    "param_description": "是否填充内部空洞",
                    "param_input_type": "selectBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [
                        {
                            "cn": "是",
                            "en": "yes",
                        },
                        {
                            "cn": "否",
                            "en": "not",
                        },
                    ],
                    "option": "yes",
                    "header_list": [],
                    "array_list": [],
                },
                {
                    "param_cn_name": "外轮廓",
                    "param_en_name": "is_contours",
                    "param_description": "是否描外轮廓",
                    "param_input_type": "selectBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [
                        {
                            "cn": "是",
                            "en": "yes",
                        },
                        {
                            "cn": "否",
                            "en": "not",
                        },
                    ],
                    "option": "not",
                    "header_list": [],
                    "array_list": [],
                }
            ]
        }
    },
    
    "30004": {
        "algorithm_id": "30004",
        "cn_name": "反色",
        "en_name": "binary",
        "description": "对logo进行反色处理，可指定前景颜色。",
        "version": "v1",
        "version_list": {
            "v1": [
                {
                    "param_cn_name": "颜色",
                    "param_en_name": "color",
                    "param_description": "前景区域的颜色",
                    "param_input_type": "multiBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [
                        {
                            "cn": "手动设定颜色",
                            "en": "manual",
                            "children":{
                                "data_type": "str",
                                "data_verify": r"^#[0-9A-Fa-f]{6,6}$",
                                "limit_low": 0,
                                "limit_high": 100,
                                # "length_min": 0,
                                # "length_max": 100,
                                "value": "#FFFFFF",
                            }
                        },
                        {
                            "cn": "跟随预定颜色",
                            "en": "follow",
                        },
                        {
                            "cn": "叠色（跟随）",
                            "en": "overlap"
                        }
                    ],
                    "option": "follow",
                    "header_list": [],
                    "array_list": [],
                },
            ]
        }
    },
    
    "30005": {
        "algorithm_id": "30005",
        "cn_name": "直接平铺",
        "en_name": "direct_tile",
        "description": "单元素网格对齐平铺。",
        "version": "v1",
        "version_list": {
            "v1": [
                {
                    "param_cn_name": "矢量路径",
                    "param_en_name": "svg_path",
                    "param_description": "svg路径，粘贴到此处",
                    "param_input_type": "textBox",
                    "data_type": "str",
                    "data_verify": r"^[Mm]+?.*[Zz]+?$",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 10000,
                    "value": "",
                    "option_list": [],
                    "option": "",
                    "header_list": [],
                    "array_list": [],
                },
                {
                    "param_cn_name": "宽高比例上限组",
                    "param_en_name": "ratio_sheet",
                    "param_description": "按照不同的宽高比，分别设置不同的缩放大小，间距大小等等",
                    "param_input_type": "arrayBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [],
                    "option": "",
                    "header_list": [
                        {
                            "column_cn_name": "宽高比上限",
                            "column_en_name": "ratio",
                            "column_description": "logo宽高比例上限",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "缩放参考基准",
                            "column_en_name": "resize_base",
                            "column_description": "等比缩放logo时，logo长边相对于框的宽或高缩放指定比例",
                            "column_input_type": "selectBox",
                            "data_type": "",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 0,
                            "option_list": [
                                {
                                    "cn": "宽",
                                    "en": "width"
                                },
                                {
                                    "cn": "高",
                                    "en": "height"
                                },
                            ],
                            "option": "width"
                        },
                        {
                            "column_cn_name": "缩放比例",
                            "column_en_name": "resize_ratio",
                            "column_description": "等比缩放logo，logo长边相对于框的宽（或高）的比例",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "横向间距参考基准",
                            "column_en_name": "h_span_base",
                            "column_description": "logo间的横向间距，基于logo的宽或高",
                            "column_input_type": "selectBox",
                            "data_type": "",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 0,
                            "option_list": [
                                {
                                    "cn": "宽",
                                    "en": "width"
                                },
                                {
                                    "cn": "高",
                                    "en": "height"
                                },
                            ],
                            "option": "width"
                        },
                        {
                            "column_cn_name": "横向间距比例",
                            "column_en_name": "h_span_ratio",
                            "column_description": "logo间的横向间距占横向间距参考基准的比例",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "纵向间距参考基准",
                            "column_en_name": "v_span_base",
                            "column_description": "logo间的纵向间距，基于logo的宽或高",
                            "column_input_type": "selectBox",
                            "data_type": "",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 0,
                            "option_list": [
                                {
                                    "cn": "宽",
                                    "en": "width"
                                },
                                {
                                    "cn": "高",
                                    "en": "height"
                                },
                            ],
                            "option": "height"
                        },
                        {
                            "column_cn_name": "纵向间距比例",
                            "column_en_name": "v_span_ratio",
                            "column_description": "logo间的纵向间距占纵向间距参考基准的比例",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "logo位于框的位置",
                            "column_en_name": "location",
                            "column_description": "logo位于框的位置",
                            "column_input_type": "selectBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [
                                {
                                    "cn": "左上",
                                    "en": "top_left",
                                },
                                {
                                    "cn": "中上",
                                    "en": "top",
                                },
                                {
                                    "cn": "右上",
                                    "en": "top_right",
                                },
                                {
                                    "cn": "左中",
                                    "en": "left",
                                },
                                {
                                    "cn": "中间",
                                    "en": "center",
                                },
                                {
                                    "cn": "右中",
                                    "en": "right",
                                },
                                {
                                    "cn": "左下",
                                    "en": "bottom_left",
                                },
                                {
                                    "cn": "中下",
                                    "en": "bottom",
                                },
                                {
                                    "cn": "右下",
                                    "en": "bottom_right",
                                },
                            ],
                            "option": "center"
                        },
                    ],
                    "array_list": [],
                },
            ]
        }
    },
    
    "30006": {
        "algorithm_id": "30006",
        "cn_name": "交错平铺",
        "en_name": "intersect_tile",
        "description": "单元素行间交错平铺。",
        "version": "v1",
        "version_list": {
            "v1": [
                {
                    "param_cn_name": "矢量路径",
                    "param_en_name": "svg_path",
                    "param_description": "svg路径，粘贴到此处",
                    "param_input_type": "textBox",
                    "data_type": "str",
                    "data_verify": r"^[Mm]+?.*[Zz]+?$",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 10000,
                    "value": "",
                    "option_list": [],
                    "option": "",
                    "header_list": [],
                    "array_list": [],
                },
                {
                    "param_cn_name": "宽高比例上限组",
                    "param_en_name": "ratio_sheet",
                    "param_description": "按照不同的宽高比，分别设置不同的缩放大小，间距大小等等",
                    "param_input_type": "arrayBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [],
                    "option": "",
                    "header_list": [
                        {
                            "column_cn_name": "宽高比上限",
                            "column_en_name": "ratio",
                            "column_description": "logo宽高比例上限",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "缩放参考基准",
                            "column_en_name": "resize_base",
                            "column_description": "等比缩放logo时，logo长边相对于框的宽或高缩放指定比例",
                            "column_input_type": "selectBox",
                            "data_type": "",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 0,
                            "option_list": [
                                {
                                    "cn": "宽",
                                    "en": "width"
                                },
                                {
                                    "cn": "高",
                                    "en": "height"
                                },
                            ],
                            "option": "width"
                        },
                        {
                            "column_cn_name": "缩放比例",
                            "column_en_name": "resize_ratio",
                            "column_description": "等比缩放logo，logo长边相对于框的宽（或高）的比例",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "横向间距参考基准",
                            "column_en_name": "h_span_base",
                            "column_description": "logo间的横向间距，基于logo的宽或高",
                            "column_input_type": "selectBox",
                            "data_type": "",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 0,
                            "option_list": [
                                {
                                    "cn": "宽",
                                    "en": "width"
                                },
                                {
                                    "cn": "高",
                                    "en": "height"
                                },
                            ],
                            "option": "width"
                        },
                        {
                            "column_cn_name": "横向间距比例",
                            "column_en_name": "h_span_ratio",
                            "column_description": "logo间的横向间距占横向间距参考基准的比例",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "纵向间距参考基准",
                            "column_en_name": "v_span_base",
                            "column_description": "logo间的纵向间距，基于logo的宽或高",
                            "column_input_type": "selectBox",
                            "data_type": "",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 0,
                            "option_list": [
                                {
                                    "cn": "宽",
                                    "en": "width"
                                },
                                {
                                    "cn": "高",
                                    "en": "height"
                                },
                            ],
                            "option": "height"
                        },
                        {
                            "column_cn_name": "纵向间距比例",
                            "column_en_name": "v_span_ratio",
                            "column_description": "logo间的纵向间距占纵向间距参考基准的比例",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "logo位于框的位置",
                            "column_en_name": "location",
                            "column_description": "logo位于框的位置",
                            "column_input_type": "selectBox",
                            "data_type": "",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [
                                {
                                    "cn": "左上",
                                    "en": "top_left",
                                },
                                {
                                    "cn": "中上",
                                    "en": "top",
                                },
                                {
                                    "cn": "右上",
                                    "en": "top_right",
                                },
                                {
                                    "cn": "左中",
                                    "en": "left",
                                },
                                {
                                    "cn": "中间",
                                    "en": "center",
                                },
                                {
                                    "cn": "右中",
                                    "en": "right",
                                },
                                {
                                    "cn": "左下",
                                    "en": "bottom_left",
                                },
                                {
                                    "cn": "中下",
                                    "en": "bottom",
                                },
                                {
                                    "cn": "右下",
                                    "en": "bottom_right",
                                },
                            ],
                            "option": "center"
                        },
                    ],
                    "array_list": [],
                },
            ]
        }
    },
    
    "30007": {
        "algorithm_id": "30007",
        "cn_name": "随机平铺",
        "en_name": "random_tile",
        "description": "单元素随机位置平铺。",
        "version": "v1",
        "version_list": {
            "v1": [
                {
                    "param_cn_name": "矢量路径",
                    "param_en_name": "svg_path",
                    "param_description": "svg路径，粘贴到此处",
                    "param_input_type": "textBox",
                    "data_type": "str",
                    "data_verify": r"^[Mm]+?.*[Zz]+?$",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 10000,
                    "value": "",
                    "option_list": [],
                    "option": "",
                    "header_list": [],
                    "array_list": [],
                },
                {
                    "param_cn_name": "平铺元素大小",
                    "param_en_name": "ele_size",
                    "param_description": "平铺纹理上logo的最大大小",
                    "param_input_type": "textBox",
                    "data_type": "float",
                    "data_verify": r"^[Mm]+?.*[Zz]+?$",
                    "limit_low": 20,
                    "limit_high": 200,
                    # "length_min": 0,
                    # "length_max": 10000,
                    "value": 100,
                    "option_list": [],
                    "option": "",
                    "header_list": [],
                    "array_list": [],
                },
                {
                    "param_cn_name": "平铺间隙大小",
                    "param_en_name": "gap_size",
                    "param_description": "平铺纹理上logo间距的大概大小",
                    "param_input_type": "selectBox",
                    "data_type": "float",
                    "data_verify": r"^[Mm]+?.*[Zz]+?$",
                    "limit_low": 20,
                    "limit_high": 200,
                    # "length_min": 0,
                    # "length_max": 10000,
                    "value": "100",
                    "option_list": [
                                {
                                    "cn": "很大",
                                    "en": "twice2"
                                },
                                {
                                    "cn": "大",
                                    "en": "twice"
                                },
                                {
                                    "cn": "标准",
                                    "en": "standard"
                                },
                                {
                                    "cn": "小",
                                    "en": "fold"
                                },
                                {
                                    "cn": "很小",
                                    "en": "fold2"
                                },
                            ],
                    "option": "standard",
                    "header_list": [],
                    "array_list": [],
                },
            ]
        }
    },
    
    "30008": {
        "algorithm_id": "30008",
        "cn_name": "虚实平铺",
        "en_name": "hollow_solid_tile",
        "description": "空心logo背景双实心logo平铺。",
        "version": "v1",
        "version_list": {
            "v1": [
                {
                    "param_cn_name": "矢量路径",
                    "param_en_name": "svg_path",
                    "param_description": "svg路径，粘贴到此处",
                    "param_input_type": "textBox",
                    "data_type": "str",
                    "data_verify": r"^[Mm]+?.*[Zz]+?$",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 10000,
                    "value": "",
                    "option_list": [],
                    "option": "",
                    "header_list": [],
                    "array_list": [],
                },
                {
                    "param_cn_name": "颜色",
                    "param_en_name": "color",
                    "param_description": "前景区域的颜色",
                    "param_input_type": "multiBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [
                        {
                            "cn": "手动设定颜色",
                            "en": "manual",
                            "children":{
                                "data_type": "str",
                                "data_verify": r"^#[0-9A-Fa-f]{6,6}$",
                                "limit_low": 0,
                                "limit_high": 100,
                                # "length_min": 0,
                                # "length_max": 100,
                                "value": "#FFFFFF",
                            }
                        },
                        {
                            "cn": "跟随预定颜色",
                            "en": "follow",
                        },
                    ],
                    "option": "follow",
                    "header_list": [],
                    "array_list": [],
                },
                {
                    "param_cn_name": "宽高比例上限组",
                    "param_en_name": "ratio_sheet",
                    "param_description": "按照不同的宽高比，分别设置不同的缩放大小，间距大小等等",
                    "param_input_type": "arrayBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [],
                    "option": "",
                    "header_list": [
                        {
                            "column_cn_name": "宽高比上限",
                            "column_en_name": "ratio",
                            "column_description": "logo宽高比例上限",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "缩放参考基准",
                            "column_en_name": "resize_base",
                            "column_description": "等比缩放logo时，logo长边相对于框的宽或高缩放指定比例",
                            "column_input_type": "selectBox",
                            "data_type": "",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 0,
                            "option_list": [
                                {
                                    "cn": "宽",
                                    "en": "width"
                                },
                                {
                                    "cn": "高",
                                    "en": "height"
                                },
                            ],
                            "option": "width"
                        },
                        {
                            "column_cn_name": "缩放比例",
                            "column_en_name": "resize_ratio",
                            "column_description": "等比缩放logo，logo长边相对于框的宽（或高）的比例",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "横向间距参考基准",
                            "column_en_name": "h_span_base",
                            "column_description": "logo间的横向间距，基于logo的宽或高",
                            "column_input_type": "selectBox",
                            "data_type": "",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 0,
                            "option_list": [
                                {
                                    "cn": "宽",
                                    "en": "width"
                                },
                                {
                                    "cn": "高",
                                    "en": "height"
                                },
                            ],
                            "option": "width"
                        },
                        {
                            "column_cn_name": "横向间距比例",
                            "column_en_name": "h_span_ratio",
                            "column_description": "logo间的横向间距占横向间距参考基准的比例",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "纵向间距参考基准",
                            "column_en_name": "v_span_base",
                            "column_description": "logo间的纵向间距，基于logo的宽或高",
                            "column_input_type": "selectBox",
                            "data_type": "",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 0,
                            "option_list": [
                                {
                                    "cn": "宽",
                                    "en": "width"
                                },
                                {
                                    "cn": "高",
                                    "en": "height"
                                },
                            ],
                            "option": "height"
                        },
                        {
                            "column_cn_name": "纵向间距比例",
                            "column_en_name": "v_span_ratio",
                            "column_description": "logo间的纵向间距占纵向间距参考基准的比例",
                            "column_input_type": "textBox",
                            "data_type": "float",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [],
                            "option": ""
                        },
                        {
                            "column_cn_name": "logo位于框的位置",
                            "column_en_name": "location",
                            "column_description": "logo位于框的位置",
                            "column_input_type": "selectBox",
                            "data_type": "",
                            "data_verify": "",
                            "limit_low": 0,
                            "limit_high": 100,
                            # "length_min": 0,
                            # "length_max": 100,
                            "value": 1,
                            "option_list": [
                                {
                                    "cn": "左上",
                                    "en": "top_left",
                                },
                                {
                                    "cn": "中上",
                                    "en": "top",
                                },
                                {
                                    "cn": "右上",
                                    "en": "top_right",
                                },
                                {
                                    "cn": "左中",
                                    "en": "left",
                                },
                                {
                                    "cn": "中间",
                                    "en": "center",
                                },
                                {
                                    "cn": "右中",
                                    "en": "right",
                                },
                                {
                                    "cn": "左下",
                                    "en": "bottom_left",
                                },
                                {
                                    "cn": "中下",
                                    "en": "bottom",
                                },
                                {
                                    "cn": "右下",
                                    "en": "bottom_right",
                                },
                            ],
                            "option": "center"
                        },
                    ],
                    "array_list": [],
                },
            ]
        }
    },
    
    "30009": {
        "algorithm_id": "30009",
        "cn_name": "旋转图像",
        "en_name": "rotate_image",
        "description": "固定图像中心旋转图像。",
        "version": "v1",
        "version_list": {
            "v1": [
                {
                    "param_cn_name": "旋转角度",
                    "param_en_name": "angle",
                    "param_description": "图像旋转角度，逆时针",
                    "param_input_type": "textBox",
                    "data_type": "float",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 360,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [],
                    "option": "",
                    "header_list": [],
                    "array_list": [],
                },
            ]
        }
    },
    

    "30010": {
        "algorithm_id": "30010",
        "cn_name": "翻转",
        "en_name": "image_flip",
        "description": "翻转logo",
        "version": "v1",
        "version_list": {
            "v1": [
                {
                    "param_cn_name": "翻转方式",
                    "param_en_name": "flip_type",
                    "param_description": "翻转方式",
                    "param_input_type": "selectBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [
                        {
                            "cn": "左右翻转",
                            "en": "left_right_flip",
                        },
                        {
                            "cn": "上下翻转",
                            "en": "top_bottom_flip",
                        },
                        {
                            "cn": "上下左右翻转",
                            "en": "top_bottom_left_right_flip",
                        },
                        {
                            "cn": "横轴纵轴调换",
                            "en": "transpose",
                        },
                    ],
                    "option": "left_right_flip",
                    "header_list": [],
                    "array_list": [],
                }
            ]
        }
    },

    "30011":{
        "algorithm_id": "30011",
        "cn_name": "深浅着色",
        "en_name": "depth_double_color",
        "description": "深背景浅前景/浅背景深前景",
        "version": "v1",
        "version_list": {
            "v1": [
                {
                    "param_cn_name": "着色方式",
                    "param_en_name": "double_color_type",
                    "param_description": "深背景浅前景/浅背景深前景",
                    "param_input_type": "selectBox",
                    "data_type": "",
                    "data_verify": "",
                    "limit_low": 0,
                    "limit_high": 100,
                    # "length_min": 0,
                    # "length_max": 100,
                    "value": 0,
                    "option_list": [
                        {
                            "cn": "深色背景浅色前景",
                            "en": "op1",
                        },
                        {
                            "cn": "浅色背景深色前景",
                            "en": "op2",
                        }
                    ],
                    "option": "op1",
                    "header_list": [],
                    "array_list": [],
                }
            ]
        }
    }
}