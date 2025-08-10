# 포도밭 작업

  
포도밭 작업은 일반 필드 작업보다 더 복잡합니다.    
최상의 작업 결과를 얻으려면 포도나무가 기본 그리드 내에서 나란히 배치되어 있어야 합니다.    
또한 각 포도나무의 시작과 끝 지점의 길이가 대략적으로 동일해야 합니다.    
  
포도밭이 기존 필드에 있는 경우, 일반 필드 작업처럼 생성기를 바로 열 수 있습니다.    
하지만 필드에 속하지 않은 경우, AI 메뉴를 통해 필드 마커를 포도나무 위에 배치해야 합니다.  


  
포도밭 작업을 위한 생성기는 옵션이 더 적습니다.    
사용하는 도구에 따라 포도나무 위에서 작업할지, 옆에서 작업할지를 선택해야 합니다.    
  
예시:  
- 기본 수확기는 포도나무 위에서 주행하며 작업해야 합니다.    
- 프리프루너(가지치기 기계)는 포도나무 왼쪽에서 주행하지만 작업은 포도나무에서 이루어지므로,    
  '포도나무에서 작업'을 선택한 후, 간격을 두고 주행해야 합니다.    
- 살포기는 포도나무 옆에서 주행하며, 왼쪽과 오른쪽 모두 살포하므로 한 줄을 건너뛰어야 합니다.  


![Image](../assets/images/vineworkgen_0_0_765_510.png)

  
포도 수확 작업은 반드시 포도나무 위에서 경로를 생성해야 합니다.    
이는 차량이 포도나무 위에서 주행하며 작업해야 하기 때문입니다.  


![Image](../assets/images/vineworkharvest_0_0_765_510.png)

  
The pre-pruner works on the vines, so the course has to be generated on the vines.  
The tool comes with an offset for the tractor, so the tractor drives between the vines.  


![Image](../assets/images/vineworkpruner_0_0_765_510.png)

  
살포기는 포도나무 옆에서 주행하며 작업을 수행합니다.    
따라서 포도나무의 왼쪽 또는 오른쪽에서 주행해야 합니다.    
살포기는 좌우 양쪽 포도나무를 동시에 작업할 수 있으므로 한 줄을 건너뛸 수 있습니다.  


![Image](../assets/images/vineworkspray_0_0_765_510.png)

