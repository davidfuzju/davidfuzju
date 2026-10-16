# CONTEXT · Tokendivers 横幅的领域语汇

本仓横幅（`assets/banner.png`，由 `banner.py` 生成）不是装饰，是 Tokendivers 的视觉断言。
本文件是这套语汇的真身——做图、写 bio、选 pinned repo 一律用这里的词，不许漂成同义词。

## 核心概念

| 术语 | 定义 | 不是什么 |
| --- | --- | --- |
| **Tokens Ocean** | token 构成的海。**token 就是海水本身**，不是海里飘的东西 | 不是"AI 的海洋"这种泛喻 |
| **洋流 line** | 一族相互平行的波浪曲线。水一直在流 | 不是各自弯曲的线——不平行就会读成曲面，画面变立体 |
| **显形** | 洋流在光照处露出 token 的真面目：被切成长短随机的 token，并分出冷暖 | 不是"越深越 token 化"——决定显形的是**照度**，不是深度 |
| **冷流 / 暖流** | 输入 token（蓝）/ 输出 token（金）。在 context 里**成段交替**：一段输入接一段输出，边界是硬的 | 不是平滑渐变，也不是逐个交错 |
| **光源** | 海底一个点光源，向外正圆发散。只有它照到的地方能看见 token | 不是锥形光柱——水下的光被散射，本来就是球 |
| **Divers** | 能看见介质本身的人。别人看见 LLM 吐出的流畅句子，Divers 看得见底下的 token | 画面里不画人：光照到哪里，Divers 的视力就到哪里 |

## 画面语法

**照度决定显形，不是深度。** 这片海一直是 token 组成的；灯外的洋流不是"还没变成 token"，是"你看不见它是 token"。

从光源往外依次退化：

> 长短随机的 token + 冷暖分色 → 无冷暖 → 完全连续的 line

### 从 Matrix 数字雨迁移

继承数字雨的哲理（世界是被渲染的 / 不可读是刻意的 / 觉醒即看穿渲染层），反转三处：

| 数字雨 | Tokens Ocean | 反转掉的 |
| --- | --- | --- |
| **雨**：从上淋下，你站在里面 | **海**：主动潜入，有深度 | 被动 → 主动 |
| 人在屏幕外隔着 CRT 看代码 | 看见的范围就是光照到的范围 | 观察 → 浸入 |
| 垂直单向下落 | 水平洋流，冷暖成段交替 | 宿命 → 交换 |

## 呈现规格

| 项 | 值 |
| --- | --- |
| 画幅 | 输出 1200 × 420，2x 导出 2400 × 840。场景画在 1900 × 720 的大画布上，再裁出窗口——光和洋流都能延伸到画外 |
| 光源位置 | 窗口右下，圆心约 90% 高。token 显形半径约 133px，圆只露出上方 2/3 |
| 背景 | 浅海 `#174A6B` → 78% 处沉到纯黑。灯外的线跟着变暗，到海底透明度退为 0 |
| 虚实 | 按照度分三档：照度低的用高斯模糊 + 低透明度，只有光照区清晰 |
| token 长度 | 短 38% / 中 54% / 长 8%，**与照度无关**——绑在照度上会让光晕外围整圈变成长条 |
| 配色 | 冷流 `#B2C6FF → #5C74D2`，暖流 `#FFE2A8 → #C48E32` |

## 已知的坑

- **`round` 线帽 + 独立 `<path>` + 透明度 < 1 = 接缝处烧出亮点**。同色同透明度的段必须合并进同一个 `<path>`，SVG 中同一 path 的自重叠不叠加 alpha
- **`str.replace` 是静默的**。改 SVG 模板必须先 `assert old in s`，否则跨行字符串匹配失败时不会报错
- 行深度要按整行 `base` 取，不能按每段实际 y——色差一跨量化档，段就被拆进不同 path，接缝重现

## 归档 · 未采用

设计过程中讨论过、最终没用上的方案，留作素材。

- **真实词句做 token**：满屏文字打乱背景表现力，改用色块表示 token
- **潜水员剪影**：在 GitHub 实际渲染尺寸下装备细节不可读；最终以光照范围代表 Divers 的视力，画面不画人
- **冷暖流迎面相撞 / 锋面下潜**：演化为平行洋流 + 成段交替

### 致敬词句池

字符集限定**中文方块字 + 拉丁字母**。日文相关已排除。

#### 东西方对位（主推：同一命题的两种语言）

人类一直在问同样的问题，只是换了字符集——而现在这些问题全变成了训练数据。

| 命题 | 中 | 西 |
| --- | --- | --- |
| 可言说的边界 | `道可道，非常道` | `Whereof one cannot speak` |
| 语言即创世 | `仓颉造字，天雨粟` | `In the beginning was the Word` |
| 模拟与真实 | `不知周之梦为蝴蝶与` | `The Matrix has you` |
| 他心问题 | `子非鱼，安知鱼之乐` | `Can machines think?` |
| 表达的极限 | `书不尽言，言不尽意` | `The limits of my language mean the limits of my world` |
| 深渊 | `北冥有鱼` | `When you gaze long into the abyss` |

#### 冷流 · 中文

`名可名，非常名`（命名即 tokenization）· `白马非马` · `上下而求索`（深潜）·
`逝者如斯夫，不舍昼夜`（流）· `上善若水` · `东临碣石，以观沧海` ·
`为有源头活水来`（训练数据的来处）· `沧海月明珠有泪`（海 + 宝藏 + 泪）· `月涌大江流`

#### 冷流 · 西文

`Call me Ishmael`（白鲸）· `The Library of Babel`（博尔赫斯）· `Ceci n'est pas une pipe`（马格利特，表征 ≠ 实物）·
`Abandon all hope, ye who enter here`（但丁地狱九层，与深度分层同构）· `Water, water, every where`（古舟子咏）·
`We are such stuff as dreams are made on` · `To be, or not to be` · `Cogito, ergo sum` ·
`shadows on the wall`（柏拉图洞穴）· `A Mathematical Theory of Communication`（香农，token 的数学根源）·
`The Analytical Engine weaves`（Ada Lovelace）· `like tears in rain`（银翼杀手，雨→海的交接点）·
`There is no spoon` · `Follow the white rabbit` · `I'm afraid I can't do that`（2001）

#### 暖流 · 机器文本

`Attention Is All You Need`（token 之所以存在的创世文档）·
`softmax` `embedding` `logits` `temperature` `top_p` `##ing` `<pad>` `</s>` `<|endoftext|>` ·
`Hello, World!` · `while (true)` · `import antigravity` · `SELECT * FROM` · `NaN` · `0x7f` · `segmentation fault`

## 未决

- 主页元数据（bio / blog / company / location）与 pinned repo —— 比横幅更影响观感
