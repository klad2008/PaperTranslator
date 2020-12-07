import GoogleTranslate

with open('test.txt', 'w', encoding = 'utf-8') as f:
    f.writelines("\t测试\n")
exit(0)

text = 'Social media has been developing rapidly in public due to its nature of spreading new information, which leads to rumors being circulated. Meanwhile, detecting rumors from such massive information in social media is becoming an arduous challenge. Therefore, some deep learning methods are applied to discover rumors through the way they spread, such as Recursive Neural Network (RvNN) and so on. However, these deep learning methods only take into account the patterns of deep propagation but ignore the structures of wide dispersion in rumor detection. Actually, propagation and dispersion are two crucial characteristics of rumors. In this paper, we propose a novel bi-directional graph model, named Bi-Directional Graph Convolutional Networks (Bi-GCN), to explore both characteristics by operating on both top-down and bottom-up propagation of rumors. It leverages a GCN with a top-down directed graph of rumor spreading to learn the patterns of rumor propagation; and a GCN with an opposite directed graph of rumor diffusion to capture the structures of rumor dispersion. Moreover, the information from source post is involved in each layer of GCN to enhance the influences from the roots of rumors. Encouraging empirical results on several benchmarks confirm the superiority of the proposed method over the state-of-the-art approaches.'
print(GoogleTranslate.translate('en', 'zh-CN', text))
