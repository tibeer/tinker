import requests
import yaml
import uvicorn

from fastapi import FastAPI

result = requests.get("https://raw.githubusercontent.com/SovereignCloudStack/standards/main/Tests/iaas/SCS-Spec.MandatoryFlavors.verbose.yaml")
try:
    standards = yaml.safe_load(result.content)["mandatory"]
except yaml.YAMLError as exc:
    print(exc)

app = FastAPI()


@app.get("/")
def main() -> dict:
    return {"mandatory": standards}


@app.post("/")
def find_flavor(
    cpus: int,
    ram: int,
    disk: int
) -> list:
    matches = []
    # find all matching flavors:
    for item in standards:
        if item["cpus"] < cpus:
            continue
        elif item["ram"] < ram:
            continue
        elif item["disk"] < disk:
            continue
        # combine values for "weight_factor"
        matches.append(
            {
                "name": item["name"],
                "cpus": item["cpus"],
                "ram": item["ram"],
                "disk": item["disk"],
                "weight_factor": item["cpus"] + item["ram"] / 1024 + item["disk"]
            }
        )

    # pick lowest siuteable flavor(s) (weight_factor)
    fitting = []
    tmp_weight = 0
    for item in sorted(matches, key=lambda weight: weight['weight_factor']):
        # first item can always be appended
        if fitting == []:
            fitting.append(
                {
                    "name": item["name"],
                    "cpus": item["cpus"],
                    "ram": item["ram"],
                    "disk": item["disk"]
                }
            )
        else:
            # check if next entry weight has the same value
            if item["weight_factor"] <= tmp_weight:
                fitting.append(item)
            else:
                break

        tmp_weight = item["weight_factor"]

    return fitting


if __name__ == "__main__":
    uvicorn.run("main:app")
