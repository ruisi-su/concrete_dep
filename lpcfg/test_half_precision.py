from lexicalizedPCFG import LexicalizedPCFG
import torch
import tqdm

# unary scores : b x n x (NT + T)
# rule scores : b x (NT+T) x (NT+T) x (NT+T)
# root_scores : b x NT
B = 4
n = 20
nt = 10
t = 20
cumulative_diff = []
init_memory_usage = []
full_memory_usage = []
half_memory_usage = []

T = 50 
tbar = tqdm.tqdm(range(T))
mean = lambda x : sum(x) / len(x) if len(x) else 0
for i in tbar:
    tbar.set_description("Mean Err: {}, Init Mem: {}, Full Mem: {}, Half Mem: {}".format(mean(cumulative_diff), 
                                                                                         mean(init_memory_usage), 
                                                                                         mean(full_memory_usage), 
                                                                                         mean(half_memory_usage)))

    lexicalizedPCFG = LexicalizedPCFG(nt, t)
    lexicalizedPCFG.huge = 1e4
    start_memory = torch.cuda.memory_allocated()
    unary_scores_hf, rule_scores_hf, root_scores_hf = torch.randn(B, n, nt + t, names=['B', 'H', 'T']).half().cuda(), \
                                            torch.randn(B, nt, n, nt + t, nt + t, 2, names=['B', 'T', 'H', 'TL', 'TR', 'D']).half().cuda(), \
                                            torch.randn(B, nt, names=['B', 'T']).half().cuda()
    unary_scores, rule_scores, root_scores = unary_scores_hf.float(), rule_scores_hf.float(), root_scores_hf.float()
    init_memory = torch.cuda.memory_allocated()
    log_Z = lexicalizedPCFG._inside(unary_scores=unary_scores, rule_scores=rule_scores, root_scores=root_scores)
    full_memory = torch.cuda.memory_allocated() - init_memory
    log_Z_hf = lexicalizedPCFG._inside(unary_scores=unary_scores_hf, rule_scores=rule_scores_hf, root_scores=root_scores_hf)
    half_memory = torch.cuda.memory_allocated() - full_memory

    diff = 2 * torch.abs(log_Z - log_Z_hf.float()) / (torch.abs(log_Z) + torch.abs(log_Z_hf.float()))
    cumulative_diff.append(diff.mean().item())
    init_memory_usage.append(init_memory)
    full_memory_usage.append(full_memory)
    half_memory_usage.append(half_memory)
