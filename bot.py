import requests
import json

# 读取地址列表的函数
def load_addresses(file_path):
    with open(file_path, "r") as f:
        # 读取文件中的每一行地址，去除可能的空白字符
        addresses = [line.strip() for line in f.readlines()]
    return addresses

# API URL
url = "https://api.clusters.xyz/v0.1/airdrops/pengu/eligibility/"

# 批量查询地址的资格及空投代币数量
def check_eligibility(addresses):
    results = []
    eligible_count = 0
    ineligible_count = 0
    failed_count = 0
    total_tokens = 0  # 总的空投代币数量
    
    for address in addresses:
        response = requests.get(f"{url}/{address}")
        
        if response.status_code == 200:
            data = response.json()
            eligible = data.get("eligible", False)
            tokens = data.get("tokens", 0)  # 获取空投代币数量，默认为 0
            details = data.get("details", "没有更多信息")
            
            results.append({
                "address": address,
                "eligible": eligible,
                "tokens": tokens,
                "details": details
            })
            
            # 统计符合资格、不符合资格、请求失败的数量
            if eligible:
                eligible_count += 1
                total_tokens += tokens  # 只有符合资格的地址才累加空投代币
            else:
                ineligible_count += 1
        else:
            results.append({
                "address": address,
                "error": f"请求失败，状态码：{response.status_code}"
            })
            failed_count += 1
    
    return results, eligible_count, ineligible_count, failed_count, total_tokens

# 主函数
def main():
    # 读取地址文件
    addresses = load_addresses("addresses.txt")  # 修改为读取 .txt 文件
    
    # 执行批量查询
    eligibility_results, eligible_count, ineligible_count, failed_count, total_tokens = check_eligibility(addresses)

    # 打印查询结果
    for result in eligibility_results:
        print(json.dumps(result, indent=4))
    
    # 输出统计信息
    print("\n查询统计：")
    print(f"符合资格的地址数量：{eligible_count}")
    print(f"不符合资格的地址数量：{ineligible_count}")
    print(f"请求失败的地址数量：{failed_count}")
    print(f"总空投代币数量：{total_tokens}")
    
    # 将结果保存为文件
    with open("eligibility_results.json", "w") as outfile:
        json.dump(eligibility_results, outfile, indent=4)

# 执行主函数
if __name__ == "__main__":
    main()
