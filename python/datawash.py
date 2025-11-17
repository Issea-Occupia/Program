raw = r"""
.bilibili.com	TRUE	/	FALSE	1788426024	buvid3	43AA53BB-8CD7-EE34-48C5-344DE258F16323338infoc
.bilibili.com	TRUE	/	FALSE	1788426024	b_nut	1756890023
.bilibili.com	TRUE	/	FALSE	1788426024	_uuid	39B24B8E-2C9B-A310D-A73D-F7C822A1A9C524289infoc
.bilibili.com	TRUE	/	FALSE	1791450025	buvid_fp	1b6de7056a7ea446be8bc42b93d11290
.bilibili.com	TRUE	/	FALSE	1793344245	enable_web_push	DISABLE
.bilibili.com	TRUE	/	FALSE	1797944309	buvid4	F5D26472-5380-E180-8C05-0F37E8812F1225204-025090317-hdxuB44/Z5Un3FWXCnnnNg%3D%3D
.bilibili.com	TRUE	/	TRUE	1774245488	DedeUserID	671440351
.bilibili.com	TRUE	/	TRUE	1774245488	DedeUserID__ckMd5	c69b333ee034101c
.bilibili.com	TRUE	/	FALSE	1794893856	theme-tip-show	SHOWED
.bilibili.com	TRUE	/	FALSE	1791450181	rpdid	|(kmJ~mumkmm0J'u~lY)m|u)|
.bilibili.com	TRUE	/	FALSE	1788513425	hit-dyn-v2	1
.bilibili.com	TRUE	/	FALSE	1788692341	theme-avatar-tip-show	SHOWED
.bilibili.com	TRUE	/	FALSE	1789832267	theme-switch-show	SHOWED
.bilibili.com	TRUE	/	FALSE	1792122430	CURRENT_BLACKGAP	0
.bilibili.com	TRUE	/	TRUE	1774245488	SESSDATA	79fd62e8%2C1774245487%2C19067%2A92CjCu0HP9-7QwdDTTIqdF8K_nmsqQq4cneUxg5H8SgcOhzk8ipQtL2KSDsXr7uEuub3sSVjlXMzJKNDJoU3ppLXpETVl6cDZTZDllRklvMC10ZDE2MHA2V3pGU3QybVkzQW1RS2N5RUlFMjhXYmhpYzl2OFB1RUl6TWNoZkprX3lfNnpZcGw4X1B3IIEC
.bilibili.com	TRUE	/	TRUE	1774245488	bili_jct	28b671222d68ce70d4e007ab6c0777ee
.bilibili.com	TRUE	/	TRUE	1774245488	sid	5yho0bmo
.bilibili.com	TRUE	/	FALSE	1794232770	LIVE_BUVID	AUTO2117596727681112
.bilibili.com	TRUE	/	FALSE	1792747117	CURRENT_QUALITY	120
.bilibili.com	TRUE	/	FALSE	1764324356	bp_video_offset_671440351	1129120939041095680
.bilibili.com	TRUE	/	FALSE	1794548961	theme_style	dark
.bilibili.com	TRUE	/	FALSE	1794745806	home_feed_column	5
.bilibili.com	TRUE	/	FALSE	1794745806	browser_resolution	1707-932
.bilibili.com	TRUE	/	FALSE	1763887375	ogv_device_support_hdr	0
www.bilibili.com	FALSE	/	FALSE	0	bmg_af_switch	1
www.bilibili.com	FALSE	/	FALSE	0	bmg_src_def_domain	i0.hdslb.com
.bilibili.com	TRUE	/	FALSE	1797750353	PVID	2
.bilibili.com	TRUE	/	FALSE	1763556214	bili_ticket	eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjM1NTYyMTIsImlhdCI6MTc2MzI5Njk1MiwicGx0IjotMX0.vGI76YBcVIweT4I1hTMB8HKAViTVLXxKL-p6SwbovyI
.bilibili.com	TRUE	/	FALSE	1763556214	bili_ticket_expires	1763556152
.bilibili.com	TRUE	/	FALSE	0	bsource	search_google
.bilibili.com	TRUE	/	FALSE	1765949841	bp_t_offset_671440351	1136102348251201536
.bilibili.com	TRUE	/	FALSE	1794893853	CURRENT_FNVAL	4048
.bilibili.com	TRUE	/	FALSE	0	b_lsid	54F961031_19A919CB8EA
"""
a = list(raw)
container = []
str_ = ''
for i in a:
    if i == '\t' or i == '\n':
        container.append(str_)
        str_ = '' 
    else:
        str_ += i
counter = 0
raw_ = []
for i in container:
    counter += 1
    if(counter % 7 == 0 or (counter - 1) % 7 == 0):
        raw_.append(i)
raw_.pop(0)
num = len(raw_)
cookies = {raw_[i]:raw_[i+1] for i in range(0, len(raw_), 2)}
print(cookies)