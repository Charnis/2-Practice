def combination(candidates, target):
    def back(start, path, remaining):
        if remaining == 0:
            result.append(path.copy())
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue  # Пропуск дубликатов
            path.append(candidates[i])
            back(i + 1, path, remaining - candidates[i])
            path.pop()

    candidates.sort()
    result = []
    back(0, [], target)
    return result

#candidates = ["Ввод чисел(через запятую)"]
candidates = [2,5,2,1,2]
target = 5
print(combination(candidates, target))